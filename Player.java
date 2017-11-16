import java.util.Random;
import java.util.Scanner;
import javax.swing.*;

import javax.swing.JOptionPane;

public class Player 
{
	Scanner scn = new Scanner(System.in);
    Random rocks = new Random();

    public enum Type{HUMAN,SMART_COMPUTER,DUMB_COMPUTER} 

    private Type type;
    
    Player()
    {
    
    }
    Player(Type x)
    {
    	type = x;
    }
    
    public void setType(Type x)
    {
    	type = x;
    }
    
    public int turn(int pileSize)
    {
    	System.out.println("pile " + pileSize);
    	int rkRemove = 0;
    	
    	switch(type)
    	{
    	case DUMB_COMPUTER:
    		rkRemove = rocks.nextInt((pileSize)/2)+1;
    		break;
    	
    	case SMART_COMPUTER:
            if(pileSize > 63)
            	rkRemove = pileSize - 63;
            else if(pileSize == 63)
            	rkRemove = rocks.nextInt((pileSize)/2)+1;
            else if(pileSize > 31)
            	rkRemove = pileSize - 31;
            else if(pileSize == 31)
            	rkRemove = rocks.nextInt((pileSize)/2)+1;
            else if(pileSize > 15)
            	rkRemove = pileSize - 15;
            else if(pileSize == 15)
            	rkRemove = rocks.nextInt((pileSize)/2)+1;
            else if (pileSize > 7)
            	rkRemove = pileSize - 7;
            else if(pileSize == 7)
            	rkRemove = rocks.nextInt((pileSize)/2)+1;
            else if(pileSize > 3)
            	rkRemove = pileSize - 3;
            else if(pileSize == 3)
            	rkRemove = rocks.nextInt((pileSize)/2)+1;
            else if(pileSize == 2)
            	rkRemove = pileSize - 1;
            else
            	rkRemove = rocks.nextInt((pileSize)/2)+1;
            break;
            
    	case HUMAN:
    		boolean correct;
    		do
	    	{
	    		if(1 <= rkRemove && rkRemove <= pileSize / 2)
	    		correct = false;
	    		else
	    		correct = true;
	    	}while(!correct);
	    		
	    		break;
    	}
    	return rkRemove;
    }
}
