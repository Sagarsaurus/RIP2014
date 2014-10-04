package rip.hw1.planner;

import rip.hw1.planner.sokoban.Problem;
import rip.hw1.planner.sokoban.SokobanHeuristic;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        String fileName;
        Problem problem;
        if(args.length == 1)
            fileName = args[0];
        else fileName = "2.txt";
        try {
            problem = new Problem(new Scanner(new File(fileName)));
            Planner planner = new AStar();
            System.out.println(problem.plan(planner, new SokobanHeuristic()));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

    }
}
