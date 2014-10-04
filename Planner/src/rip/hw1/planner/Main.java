package rip.hw1.planner;

import java.io.File;

public class Main {

    public static void main(String[] args) {
        String fileName = args[0];
        Problem problem = new Problem(new File(fileName));

    }
}
