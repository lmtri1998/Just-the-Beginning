import javax.swing.*;

import java.awt.Checkbox;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.event.*;
import javax.swing.*;
import java.util.*;
import java.util.Timer;

public class Interface extends JPanel{
	Player player = new Player();
    Player humanPlayer = new Player(Player.Type.HUMAN);
    Player compPlayer = new Player(Player.Type.SMART_COMPUTER);
    Player secondPlayer = new Player(Player.Type.HUMAN);
    Player firstPlayer = new Player(Player.Type.HUMAN);
    private int pile = (int)(Math.random()*89)+11;
    private int turn;
    Random rand = new Random();
    private JLabel label1,choice,first,pileOFRock,removeComp,removeHuman, warning;
    private JTextField player1;
    private JPanel panel1, panel2;
    private JRadioButton pvp, dbot, sbot;
    private int rockTaken = 0;
    
    public Interface()
    {
    	turn = rand.nextInt(2);
    	panel1 = new JPanel();
    	panel1.setBackground(Color.gray);
		panel1.setPreferredSize(new Dimension(500,250));
		
		panel2 = new JPanel();
		panel2.setBackground(Color.gray);
		panel2.setPreferredSize(new Dimension(250,250));
		
		choice = new JLabel("Choose a game mode: ");
		
		pvp = new JRadioButton("Player vs Player");
		pvp.setActionCommand("Player vs Player");
		pvp.addActionListener(new ChoicesListener());
		
		dbot = new JRadioButton("Player vs Dumb Bot");
		dbot.setActionCommand("Player vs Dumb Bot");
		dbot.addActionListener(new ChoicesListener());
		
		sbot = new JRadioButton("Player vs Smart Bot");
		sbot.setActionCommand("Player vs Smart Bot");
		sbot.addActionListener(new ChoicesListener());
		
		first = new JLabel("");
		
		 ButtonGroup group = new ButtonGroup();
		    group.add(pvp);
		    group.add(dbot);
		    group.add(sbot);
		
		    
		panel2.add(choice);
		panel2.add(first);
		panel2.add(pvp);
		panel2.add(dbot);
		panel2.add(sbot);
		panel2.add(first);
    	add(panel1);
		add(panel2);

    }
    public void humanPlay()
    {
    	if(!pvp.isSelected())
    	{
	    	rockTaken = 0;
	    	humanPlayer.turn(pile);
			rockTaken = Integer.parseInt(player1.getText());
			System.out.println("Human" + rockTaken);
			if(1 <=  rockTaken && rockTaken < ((pile/2)+1))
			{
				pile = pile - rockTaken;
		        removeHuman.setText(" You removed " + rockTaken + " rocks last turn."); 
				pileOFRock.setText(pile + " rocks left.");
				player1.setText("");
	        	
			}
			else
			{
				warning.setText("Please choose a number between 1 and " + pile/2);
		  		JOptionPane.showMessageDialog(null, "You must take a number between 1 and " + pile/2);
		  		player1.setText("");
		  		rockTaken = Integer.parseInt(player1.getText());
			}
    	}
    	else
    	{
    		if(turn == 0)
    		{
    			rockTaken = 0;
    	    	humanPlayer.turn(pile);
    			rockTaken = Integer.parseInt(player1.getText());
    			System.out.println("Human" + rockTaken);
    			label1.setText("Player 1");
    			warning.setText("Player1, please choose the numbers of rocks between 1 and "  + pile/2);
    			if(1 <=  rockTaken && rockTaken < ((pile/2)+1))
    			{
    				pile = pile - rockTaken;
    		        removeHuman.setText(" Player 1 removed " + rockTaken + " rocks on their last turn."); 
    				pileOFRock.setText(pile + " rocks left.");
    				player1.setText("");
    				label1.setText("Player 2");
    				warning.setText("Player2 turn, please choose the numbers of rocks between 1 and "  + pile/2);
    	        	
    			}
    			else
    			{
    				warning.setText("Player1, please choose the numbers of rocks between 1 and "  + pile/2);
    		  		JOptionPane.showMessageDialog(null, "You must take a number between 1 and " + pile/2);
    		  		player1.setText("");
    		  		rockTaken = Integer.parseInt(player1.getText());
    			}
    		}
    		else
    		{
    			rockTaken = 0;
    	    	humanPlayer.turn(pile);
    			rockTaken = Integer.parseInt(player1.getText());
    			System.out.println("Human" + rockTaken);
    			label1.setText("Player 2");
    			warning.setText("Player2, please choose the numbers of rocks between 1 and "  + pile/2);
    			if(1 <=  rockTaken && rockTaken < ((pile/2)+1))
    			{
    				pile = pile - rockTaken;
    		        removeHuman.setText(" Player 2 removed " + rockTaken + " rocks on their last turn."); 
    				pileOFRock.setText(pile + " rocks left.");
    				player1.setText("");
    				label1.setText("Player 1");
    				warning.setText("Player1 turn, please choose the numbers of rocks between 1 and "  + pile/2);
    	        	
    			}
    			else
    			{
    				warning.setText("Player2, please choose the numbers of rocks between 1 and "  + pile/2);
    		  		JOptionPane.showMessageDialog(null, "You must take a number between 1 and " + pile/2);
    		  		player1.setText("");
    		  		rockTaken = Integer.parseInt(player1.getText());
    			}
    		}
    	}
    }
    public void compPlay()
    {
    	rockTaken = 0;
    	rockTaken  = compPlayer.turn(pile);
    	System.out.println(" Computer" + rockTaken);
		removeComp.setText(" Computer removed " + rockTaken + " rocks last turn.");
		pile = pile - rockTaken;
		pileOFRock.setText(pile + " rocks left.");
		warning.setText("Please choose a number between 1 and " + pile/2);
    	
    }

    private class ChoicesListener implements ActionListener
    {
    	public void actionPerformed(ActionEvent e)
    	{
    		if(sbot.isSelected())
    		{ 
                compPlayer.setType(Player.Type.SMART_COMPUTER);
                panel2.remove(pvp);
                panel2.remove(dbot);
                panel2.remove(sbot);

                choice.setText("Playing against smart mode computer!");
                
                label1 = new JLabel("Human");
        		warning = new JLabel("Please choose the numbers of rocks between 1 and "  + pile/2);
        		pileOFRock = new JLabel("Initial pile contains " + pile + " rocks.");
        		removeComp = new JLabel("");
        		removeHuman = new JLabel("");
        		player1 = new JTextField(10);
        		player1.addActionListener(new GameListener());

        		panel1.add(label1);
        		panel1.add(player1);
        		panel1.add(warning);
        		panel1.add(removeHuman);
        		
        		panel2.add(pileOFRock);
        		panel2.add(removeComp);
            }
            else if(dbot.isSelected())
            {
                compPlayer.setType(Player.Type.DUMB_COMPUTER);
                panel2.remove(pvp);
                panel2.remove(dbot);
                panel2.remove(sbot);

                choice.setText("Playing against dumb mode computer!");
                label1 = new JLabel("Human");
        		warning = new JLabel("Please choose the numbers of rocks between 1 and "  + pile/2);
        		pileOFRock = new JLabel("Initial pile contains " + pile + " rocks.");
        		removeComp = new JLabel("");
        		removeHuman = new JLabel("");
        		player1 = new JTextField(10);
        		player1.addActionListener(new GameListener());

        		panel1.add(label1);
        		panel1.add(player1);
        		panel1.add(warning);
        		panel1.add(removeHuman);
        		
        		panel2.add(pileOFRock);
        		panel2.add(removeComp);
                
            }
            else
            {
            	choice.setText("It's a PvP!");
            	panel2.remove(pvp);
                panel2.remove(dbot);
                panel2.remove(sbot);

            	compPlayer = humanPlayer;
            	label1 = new JLabel("Human");
        		warning = new JLabel("");
        		pileOFRock = new JLabel("Initial pile contains " + pile + " rocks.");
        		removeHuman = new JLabel("");
        		player1 = new JTextField(10);
        		player1.addActionListener(new GameListener());

        		panel1.add(label1);
        		panel1.add(player1);
        		panel1.add(warning);
        		panel1.add(removeHuman);

        		
        		panel2.add(pileOFRock);
               
            }

            if(!pvp.isSelected())
            {	
	    		if(turn == 1)
	    		{
	            	first.setText("You go first.");
	            	firstPlayer = humanPlayer; 
	                secondPlayer = compPlayer;
	                humanPlay();
	                turn = (pile > 0 ? turn == 1 ? 0 : 1 : turn);
	            }
	
	            else
	            {
	                first.setText("Computer go first.");
	                firstPlayer = compPlayer;
	                secondPlayer = humanPlayer;
	                compPlay();
	                turn = (pile > 0 ? turn == 1 ? 0 : 1 : turn);
	            } 		
            }
            else
            {
            	if(turn == 1)
	    		{
	            	first.setText("Player 2 go first.");
	            	firstPlayer = humanPlayer; 
	                secondPlayer = humanPlayer;
	                label1.setText("Player 2");
	                warning.setText("Player2, please choose the numbers of rocks between 1 and "  + pile/2);
	                humanPlay();
	                turn = (pile > 0 ? turn == 1 ? 0 : 1 : turn);
	            }
	
	            else
	            {
	                first.setText("Player 1 go first.");
	                firstPlayer = humanPlayer;
	                secondPlayer = humanPlayer;
	                label1.setText("Player 1");
	                warning.setText("Player1, please choose the numbers of rocks between 1 and "  + pile/2);
	                humanPlay();
	                turn = (pile > 0 ? turn == 1 ? 0 : 1 : turn);
	            }
            }  
    	}
    }
    private class GameListener implements ActionListener
    {
    	public void actionPerformed(ActionEvent e)
    	{        
    		first.setText("");
			choice.setText("");
			
			panel2.remove(first);
    		panel2.remove(choice);
    		if(!pvp.isSelected())
    		{
	    		while(pile > 1)
	    		{
	    			if(turn == 0)
	    			{
	    				compPlay();	
	    				turn = 1;
	    			}    			
	    			else
	    			{
	    				humanPlay();
	    				turn = 0;
	    			}
	    		}
	    		if(pile == 1 && turn == 1)
	        	{ 
	        		pileOFRock.setText("**********Computer wins.**********");
	        		removeComp.setText("");
	        		removeHuman.setText("");
	        	}
	    		if(pile == 1 && turn == 0)
	        	{ 
	        		pileOFRock.setText("**********You win.**********");
	        		removeHuman.setText("");
	        		removeComp.setText("");
	        	}
    		}
    		else
    		{
    			
	    		while(pile > 1)
	    		{
	    			if(turn == 0)
	    			{
	    				humanPlay();	
	    				turn = 1;
	    			}    			
	    			else
	    			{
	    				humanPlay();
	    				turn = 0;
	    			}
	    		}
	    		if(pile == 1 && turn == 0)
	        	{ 
	        		pileOFRock.setText("**********Player 2 wins.**********");
	        		removeComp.setText("");
	        		removeHuman.setText("");
	        	}
	    		if(pile == 1 && turn == 1)
	        	{ 
	        		pileOFRock.setText("**********Player 1 wins.**********");
	        		removeHuman.setText("");
	        		removeComp.setText("");
	        	}
    		}
    	}
    }
}   

