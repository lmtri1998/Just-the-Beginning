"""Assignment 1 - Bike-share objects

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Station and Ride classes, which store the data for the
objects in this simulation.

There is also an abstract Drawable class that is the superclass for both
Station and Ride. It enables the simulation to visualize these objects in
a graphical window.
"""
from datetime import datetime
from typing import Tuple


# Sprite files
STATION_SPRITE = 'stationsprite.png'
RIDE_SPRITE = 'bikesprite.png'


class Drawable:
    """A base class for objects that the graphical renderer can be drawn.

    === Public Attributes ===
    sprite:
        The filename of the image to be drawn for this object.
    """
    sprite: str

    def __init__(self, sprite_file: str) -> None:
        """Initialize this drawable object with the given sprite file.
        """
        self.sprite = sprite_file

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (lat, long) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    capacity:
        the total number of bikes the station can store
    location:
        the location of the station in lat/long coordinates
    name: str
        name of the station
    num_bikes: int
        current number of bikes at the station
    leave: float
        number of bikes leave the station
    arrive: float
        number of bikes arrive at the station
    time_low_bikes: float
        time spent with at most five bikes
    time_low_vacant: float
        time spent with at most five unoccupied spots

    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    """
    name: str
    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    leave: float
    arrive: float
    time_low_bikes: float
    time_low_vacant: float

    def __init__(self, pos: Tuple[float, float], cap: int,
                 num_bikes: int, name: str) -> None:
        """Initialize a new station.

        Precondition: 0 <= num_bikes <= cap
        """
        Drawable.__init__(self, STATION_SPRITE)
        self.location = pos
        self.capacity = cap
        self.num_bikes = num_bikes
        self.name = name
        self.time_low_bikes = 0.0
        self.time_low_vacant = 0.0
        self.leave = 0.0
        self.arrive = 0.0

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (lat, long) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        return self.location

    def check_num_bikes(self) -> bool:
        """Return the boolean to see if num_bikes <= 5"""
        return self.num_bikes <= 5

    def check_vacancy(self) -> bool:
        """Return the boolean to see if unoccupied spot <= 5"""
        return (self.capacity - self.num_bikes) <= 5


class Ride(Drawable):
    """A ride using a Bixi bike.

    === Attributes ===
    start:
        the station where this ride starts
    end:
        the station where this ride ends
    start_time:
        the time this ride starts
    end_time:
        the time this ride ends

    === Representation Invariants ===
    - start_time < end_time
    """
    start: Station
    end: Station
    start_time: datetime
    end_time: datetime

    def __init__(self, start: Station, end: Station,
                 times: Tuple[datetime, datetime]) -> None:
        """Initialize a ride object with the given start and end information.
        """
        Drawable.__init__(self, RIDE_SPRITE)
        self.start, self.end = start, end
        self.start_time, self.end_time = times[0], times[1]

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.
        """
        # Calculate the distance between the start point and end point longitude
        # and latitude.
        distance_lo = self.end.location[0] - self.start.location[0]
        distance_la = self.end.location[1] - self.start.location[1]
        # Use the ratio between the time taken to travel to the point and
        # time taken to travel the whole trip to calculate the position.
        total_time = self.end_time - self.start_time
        current_time = time - self.start_time
        ratio = (current_time.total_seconds())/(total_time.total_seconds())
        new_lo_pos = self.start.location[0] + (distance_lo * ratio)
        new_la_pos = self.start.location[1] + (distance_la * ratio)

        return (new_lo_pos, new_la_pos)

    def add_leave(self, time: datetime):
        """Add to the amount of bikes leave and decrement the number of bikes in
        the station. Only the rides that start during the simulation will count.
        """
        if time == self.start_time:
            self.start.leave += 1.0
            self.start.num_bikes -= 1

    def add_arrive(self):
        """Add to the amount of bikes arrive and increment the number of bikes
        in the station. Only increment the statistics if there is space in the
        station.
        """
        if self.end.num_bikes < self.end.capacity:
            self.end.arrive += 1.0
            self.end.num_bikes += 1


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'
        ],
        'max-attributes': 15
    })
