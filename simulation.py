"""Assignment 1 - Simulation

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Simulation class, which is the main class for your
bike-share simulation.

At the bottom of the file, there is a sample_simulation function that you
can use to try running the simulation at any time.
"""
import csv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

from bikeshare import Ride, Station
from container import PriorityQueue
from visualizer import Visualizer

# Datetime format to parse the ride data
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


class Simulation:
    """Runs the core of the simulation through time.

    === Attributes ===
    all_rides:
        A list of all the rides in this simulation.
        Note that not all rides might be used, depending on the timeframe
        when the simulation is run.
    all_stations:
        A dictionary containing all the stations in this simulation.
    visualizer:
        A helper class for visualizing the simulation.
    active_rides:
        A list to keep track of the rides that are in progress at the current
        time in the simulation.
    queue:
        A queue to keep track of of when rides become active or inactive.
    """
    all_stations: Dict[str, Station]
    all_rides: List[Ride]
    visualizer: Visualizer
    active_rides: List[Ride]
    queue: PriorityQueue

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.visualizer = Visualizer()
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.active_rides = []
        self.queue = PriorityQueue()

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        """
        step = timedelta(minutes=1)  # Each iteration spans one minute of time

        # Add the rides into the queue.
        for r in self.all_rides:
            if r.start_time <= end and r.end_time >= start:
                ride_start = RideStartEvent(self, r.start_time, r)
                self.queue.add(ride_start)

        # Main run simulation loop.
        current_time = start
        while current_time <= end:
            # Update the rides.
            self._update_active_rides_fast(current_time)

            # Draw the map, the rides, and the stations.
            everything_list = \
                list(self.all_stations.values()) + self.active_rides
            self.visualizer.render_drawables(everything_list, current_time)

            # Add to the time spent with low number of bikes and/or low number
            # of vacant spot <= 5.
            for s in self.all_stations:
                if self.all_stations[s].check_num_bikes() \
                        and current_time < end:
                    self.all_stations[s].time_low_bikes += step.total_seconds()
                if self.all_stations[s].check_vacancy() \
                        and current_time < end:
                    self.all_stations[s].time_low_vacant += step.total_seconds()

            current_time += step
        # Leave this code at the very bottom of this method.
        # It will keep the visualization window open until you close
        # it by pressing the 'X'.
        while True:
            if self.visualizer.handle_window_events():
                return  # Stop the simulation

    def _update_active_rides(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   Loop through `self.all_rides` and compare each Ride's start and
            end times with <time>.

            If <time> is between the ride's start and end times (inclusive),
            then add the ride to self.active_rides if it isn't already in
            that list.

            Otherwise, remove the ride from self.active_rides if it is in
            that list.

        -   This means that if a ride started before the simulation's time
            period but ends during or after the simulation's time period,
            it should still be added to self.active_rides.
        """
        for r in self.all_rides:
            if r.start_time <= time <= r.end_time:
                if r not in self.active_rides and r.start.num_bikes > 0:
                    r.add_leave(time)
                    self.active_rides.append(r)
            elif r.end_time <= time:
                if r in self.active_rides:
                    r.add_arrive()
                    self.active_rides.remove(r)

    def calculate_statistics(self) -> Dict[str, Tuple[str, float]]:
        """Return a dictionary containing statistics for this simulation.
        The returned dictionary has exactly four keys, corresponding
        to the four statistics tracked for each station:
          - 'max_start'
          - 'max_end'
          - 'max_time_low_availability'
          - 'max_time_low_unoccupied'

        The corresponding value of each key is a tuple of two elements,
        where the first element is the name (NOT id) of the station that has
        the maximum value of the quantity specified by that key,
        and the second element is the value of that quantity.

        For example, the value corresponding to key 'max_start' should be the
        name of the station with the most number of rides started at that
        station, and the number of rides that started at that station.
        """
        # Create empty dictionaries to store the neccessary values from the
        # stations.
        d_start = {}
        d_end = {}
        d_low_availability = {}
        d_low_unoccupied = {}

        # Use stations'name as the dictionaries' key.
        # The value of each dictionary will be the amount of bike leave,
        # the amount of bike arrive, the amount of time spent with low number of
        # bikes and the amount of unoccupied spot of each stations respectively.
        for s in self.all_stations:
            current_name = self.all_stations[s].name
            d_start[current_name] = self.all_stations[s].leave
            d_end[current_name] = self.all_stations[s].arrive
            d_low_availability[current_name] = \
                self.all_stations[s].time_low_bikes
            d_low_unoccupied[current_name] = \
                self.all_stations[s].time_low_vacant

        # Find the maximum values, store them into these varibles respectively:
        #  - 'max_start'
        #  - 'max_end'
        #  - 'max_time_low_availability'
        #  - 'max_time_low_unoccupied'
        #  and return them in form of a Dict[str, Tuple[str, float]].
        max_start = find_maximum(d_start)
        max_end = find_maximum(d_end)
        max_time_low_availability = find_maximum(d_low_availability)
        max_time_low_unoccupied = find_maximum(d_low_unoccupied)
        return {
            'max_start': max_start,
            'max_end': max_end,
            'max_time_low_availability': max_time_low_availability,
            'max_time_low_unoccupied': max_time_low_unoccupied
        }

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   see Task 5 of the assignment handout
        """
        # Loop through the queue
        while not self.queue.is_empty():
            event = self.queue.remove()
            if event.time > time:
                self.queue.add(event)
                break
            else:
                event_num_bikes = event.ride.start.num_bikes
                if isinstance(event, RideStartEvent) and event_num_bikes > 0:
                    event.ride.add_leave(time)
                    end_event = event.process()
                    self.queue.add(end_event[0])
                if isinstance(event, RideEndEvent):
                    event.process()


def find_maximum(current_dict: Dict[str, float]) -> Tuple[str, float]:
    """ This function find the key with the maximum value in the dictionary and
    return them as a Tuple[str, float].

    >>> ran_dict = {'fred': 2.0, 'arju': 1.0, 'monalisa': 2.0, 'hat': 0.0}
    >>> find_maximum(ran_dict)
    ('fred', 2.0)
    """
    max_val = 0.0
    max_val_name = ''
    for k in current_dict:
        if current_dict[k] > max_val:
            max_val = current_dict[k]
            max_val_name = k
        elif current_dict[k] == max_val:
            if max_val_name > k:
                max_val_name = k
            elif max_val_name == '':
                max_val_name = k

    return (max_val_name, max_val)


def create_stations(stations_file: str) -> Dict[str, 'Station']:
    """Return the stations described in the given JSON data file.

    Each key in the returned dictionary is a station id,
    and each value is the corresponding Station object.
    Note that you need to call Station(...) to create these objects!

    Precondition: stations_file matches the format specified in the
                  assignment handout.

    This function should be called *before* _read_rides because the
    rides CSV file refers to station ids.
    """
    # Read in raw data using the json library.
    with open(stations_file) as file:
        raw_stations = json.load(file)

    stations = {}
    for s in raw_stations['stations']:
        # Extract the relevant fields from the raw station JSON.
        # s is a dictionary with the keys 'n', 's', 'la', 'lo', 'da', and 'ba'
        # as described in the assignment handout.
        # NOTE: all of the corresponding values are strings, and so you need
        # to convert some of them to numbers explicitly using int() or float().
        id_ = s['n']
        pos = (float(s['lo']), float(s['la']))
        capacity = int(s['da']) + int(s['ba'])
        num_bikes = int(s['da'])
        name = s['s']
        stations[id_] = Station(pos, capacity, num_bikes, name)

    return stations


def create_rides(rides_file: str,
                 stations: Dict[str, 'Station']) -> List['Ride']:
    """Return the rides described in the given CSV file.

    Lookup the station ids contained in the rides file in <stations>
    to access the corresponding Station objects.

    Ignore any ride whose start or end station is not present in <stations>.

    Precondition: rides_file matches the format specified in the
                  assignment handout.
    """
    rides = []
    with open(rides_file) as file:
        for line in csv.reader(file):
            # line is a list of strings, following the format described
            # in the assignment handout.
            #
            # Convert between a string and a datetime object
            # using the function datetime.strptime and the DATETIME_FORMAT
            # constant we defined above. Example:
            # >>> datetime.strptime('2017-06-01 8:00', DATETIME_FORMAT)
            # datetime.datetime(2017, 6, 1, 8, 0)
            if line[1] in stations and line[3] in stations:
                start = line[1]
                end = line[3]
                start_time = datetime.strptime(line[0], DATETIME_FORMAT)
                end_time = datetime.strptime(line[2], DATETIME_FORMAT)
                time = (start_time, end_time)
                r = Ride(stations[start], stations[end], time)
                rides.append(r)

    return rides


class Event:
    """An event in the bike share simulation.

    Events are ordered by their timestamp.
    """
    simulation: 'Simulation'
    time: datetime

    def __init__(self, simulation: 'Simulation', time: datetime) -> None:
        """Initialize a new event."""
        self.simulation = simulation
        self.time = time

    def __lt__(self, other: 'Event') -> bool:
        """Return whether this event is less than <other>.

        Events are ordered by their timestamp.
        """
        return self.time < other.time

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        raise NotImplementedError


class RideStartEvent(Event):
    """An event corresponding to the start of a ride.

    === Attributes ===
    ride: Ride
        store the ride that this event is associate to.
    """
    ride: Ride

    def __init__(self, simulation: 'Simulation',
                 time: datetime, ride: Ride) -> None:
        """Initialize a start event."""
        Event.__init__(self, simulation, time)
        self.ride = ride

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.
        Add a ride into the list of active ride in the simulation.
        Return a list of new events spawned by this event.
        """
        new_event = []
        self.simulation.active_rides.append(self.ride)
        end_event = RideEndEvent(self.simulation, self.ride.end_time, self.ride)
        new_event.append(end_event)
        return new_event


class RideEndEvent(Event):
    """An event corresponding to the start of a ride.

    === Attributes ===
    ride: Ride
        store the ride that this event is associate to.
    """
    ride: Ride

    def __init__(self, simulation: 'Simulation',
                 time: datetime, ride: Ride) -> None:
        """Initialize a start event."""
        Event.__init__(self, simulation, time)
        self.ride = ride

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.
        Remove the ride from the list of active ride in the simulation
        and increment the arrive attribute and the amount of bikes in the
        station. Return an empty list because it does not generate any new
        event.
        """
        new_event = []
        self.ride.add_arrive()
        self.simulation.active_rides.remove(self.ride)

        return new_event


def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""
    sim = Simulation('stations.json', 'sample_rides.csv')
    sim.run(datetime(2017, 6, 1, 8, 00, 0),
            datetime(2017, 6, 1, 9, 00, 0))
    return sim.calculate_statistics()


if __name__ == '__main__':
    # Uncomment these lines when you want to check your work using python_ta!
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['create_stations', 'create_rides'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'csv', 'datetime', 'json',
            'bikeshare', 'container', 'visualizer'
        ]
    })
    print(sample_simulation())
