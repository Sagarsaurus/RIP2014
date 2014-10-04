package rip.hw1.planner;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        String fileName;
        Problem problem;
        if(args.length == 1)
            fileName = args[0];
        else fileName = "1.txt";
        try {
            problem = new Problem(new Scanner(new File(fileName)));
            Planner planner = new AStar();
            System.out.println(planner.run(problem.getStart(), problem.getGoal()));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

    }
}
