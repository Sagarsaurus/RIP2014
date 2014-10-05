package rip.hw1.planner;
import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;
import java.util.LinkedList;
/**
 * Created by ajmalkunnummal on 10/3/14.
 */
public class AStar implements Planner {
    private boolean goalReached = false;
    @Override
    public Object[] run(State start, State end, Heuristic heuristic) {
        PriorityQueue<State> pq = new PriorityQueue<State>();
        List<State> visited = new ArrayList<State>();
        pq.add(start);
        while(!pq.isEmpty()) {
            State current = pq.poll();
            if(current.same(end)) {
                return current.getActions();
            }
            visited.add(current);
            for(State s : current.neighbours()) {
                if(!visited.contains(s)) {
                    s.setTentativeDistance(s.getActions().length + heuristic.estimate(s,end));
                    pq.add(s);
                }
            }
        }
        return null;
    }
}
