package rip.hw1.planner;
import java.util.PriorityQueue;
import java.util.LinkedList;
/**
 * Created by ajmalkunnummal on 10/3/14.
 */
public class AStar implements Planner {
    private boolean goalReached = false;
    @Override
    public Object[] run(State start, State end, Heuristic heuristic) {
        Priority<State> pq = new PriorityQueue<State>();
        LinkedList<State> visited = new LinkedList<State>();
        pq.add(start);
        while(!goalReached || !pq.isEmpty()) {
            State current = pq.poll();
            if current.equals(end) {
                goalReached = true;
            }

            else {
                visited.add(current);
                for(State s : current.neighbours()) {
                    if(!visited.contains(s)) {
                        s.setTentativeDistance(s.getActions.length + heuristic.estimate(s,end));
                        pq.add(s);
                    }
                }
            }
        }

        if(goalReached) {
            return end.getActions();
        }

        else {
            System.out.println("Goal state not found");
            return null;
        }
    }
}
