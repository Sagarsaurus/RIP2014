package rip.hw1.planner.sokoban;

import rip.hw1.planner.Heuristic;
import rip.hw1.planner.State;
import static java.lang.Math.*;

/**
 * Created by ajmalkunnummal on 10/3/14.
 */
public class SokobanHeuristic implements Heuristic {
    @Override
    public double estimate(State start, State goal) {
    	double sum=0;
        for(i=0;i<start.boxes.length;i++){
        	sum+=Math.abs(start.boxes[i].x-goal.boxes[i].x)
        	sum+=Math.abs(start.boxes[i].y-goal.boxes[i].y)
        }
        return sum;
        
    }
}
