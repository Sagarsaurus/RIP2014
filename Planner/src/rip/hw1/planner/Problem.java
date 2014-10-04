package rip.hw1.planner;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Created by ajmalkunnummal on 10/3/14.
 */
public class Problem {
    private SokobanState start, goal;
    private boolean[][] walls;
    public Problem(Scanner problem){
        int x = problem.nextInt(), y = problem.nextInt(), n = problem.nextInt();
        String robot = problem.nextLine();
        List<String>    boxes = new ArrayList<String>(n),
                        goals = new ArrayList<String>(n);
        for(int i = 0; i < n; i++)
            boxes.add(problem.nextLine());
        for(int i = 0; i < n; i++)
            goals.add(problem.nextLine());
        walls = new boolean[x][y];
        for(int i = 0; i < x; i++) {
            String line[] = problem.nextLine().split(" ");
            for(int j = 0; j < y; j++) {
                walls[i][j] = Integer.parseInt(line[j]) == 0;
            }
        }
        start = new SokobanState(walls, robot, boxes);
        goal = new SokobanState(walls, robot, goals);
    }
    public State getStart(){
        return start;
    }
    public State getGoal(){
        return goal;
    }
}
