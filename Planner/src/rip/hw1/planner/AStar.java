package rip.hw1.planner;

/**
 * Created by ajmalkunnummal on 10/3/14.
 */
public class AStar implements Planner {
    @Override
    public Object[] run(State start, State end, Heuristic heuristic) {
        return start.getActions();
    }
}
