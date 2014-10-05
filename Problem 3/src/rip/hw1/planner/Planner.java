package rip.hw1.planner;

/**
 * Created by ajmalkunnummal on 10/3/14.
 */
public interface Planner {
    public Object[] run(State start, State end, Heuristic heuristic);
}
