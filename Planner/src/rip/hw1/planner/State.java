package rip.hw1.planner;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by ajmalkunnummal on 10/3/14.
 */
public class State {
    private class Item implements Comparable{
        private String name;
        private int x, y;
        private boolean moveable, pushable;
        public Item(String name, int x, int y, boolean moveable, boolean pushable){
            this.name = name;
            this.x = x;
            this.y = y;
            this.moveable = moveable;
            this.pushable = pushable;
        }
        public Item(Item item){
            this(item.name, item.x, item.y, item.moveable, item.pushable);
        }
        public boolean equals(Item item){
            return  item.name.equals(name) &&
                    item.x == x &&
                    item.y == y;
        }
        public boolean same(Item item){
            return item.name.equals(name);
        }

        @Override
        public int compareTo(Object item) {
            return name.compareTo( ((Item)item).name);
        }
    }
    private Item robot;
    private Item[] boxes; // Always kept sorted
    private Item[][] itemGrid;
    private int gridW, gridH;
    boolean[][] walls;

    public State(String items[]){
        //TODO
    }
    public State(State state){
        gridH = state.gridH;
        gridW = state.gridW;
        itemGrid = new Item[gridW][gridH];
        walls = state.walls;
        robot = new Item(state.robot);
        itemGrid[robot.x][robot.y] = robot;
        boxes = new Item[state.boxes.length];
        for(int i = 0; i < boxes.length; i++) {
            boxes[i] = new Item(state.boxes[i]);
        }
    }
    public boolean equals(State state){
        if(!robot.equals(state.robot))
            return false;
        if(state.boxes.length != boxes.length)
            return false;
        for(int i = 0; i < boxes.length; i++){
            if(!state.boxes[i].equals(boxes[i]))
                return false;
        }
        return true;
    }

    public List<State> neighbours(){
        List<State> neighbours = new ArrayList<State>();
        if(!walls[robot.x + 1][robot.y]) {
            if(itemGrid[robot.x + 1][robot.y] == null) {
                State n = new State(this);
                n.move(n.robot, 1, 0);
                neighbours.add(n);
            }
            else if(!walls[robot.x + 2][robot.y] && itemGrid[robot.x + 2][robot.y] == null) {
                State n = new State(this);
                n.move(itemGrid[robot.x + 1][robot.y], 1, 0);
                n.move(n.robot, 1, 0);
                neighbours.add(n);
            }
        }
        if(!walls[robot.x - 1][robot.y]) {
            if(itemGrid[robot.x - 1][robot.y] == null) {
                State n = new State(this);
                n.move(n.robot, -1, 0);
                neighbours.add(n);
            }
            else if(!walls[robot.x - 2][robot.y] && itemGrid[robot.x - 2][robot.y] == null) {
                State n = new State(this);
                n.move(itemGrid[robot.x - 1][robot.y], -1, 0);
                n.move(n.robot, -1, 0);
                neighbours.add(n);
            }
        }
        if(!walls[robot.x][robot.y + 1]) {
            if(itemGrid[robot.x][robot.y + 1] == null) {
                State n = new State(this);
                n.move(n.robot, 0, 1);
                neighbours.add(n);
            }
            else if(!walls[robot.x][robot.y + 2] && itemGrid[robot.x][robot.y + 2] == null) {
                State n = new State(this);
                n.move(itemGrid[robot.x][robot.y + 1], 0, 1);
                n.move(n.robot, 0, 1);
                neighbours.add(n);
            }
        }
        if(!walls[robot.x][robot.y - 1]) {
            if(itemGrid[robot.x][robot.y - 1] == null) {
                State n = new State(this);
                n.move(n.robot, 0, -1);
                neighbours.add(n);
            }
            else if(!walls[robot.x][robot.y - 2] && itemGrid[robot.x][robot.y - 2] == null) {
                State n = new State(this);
                n.move(itemGrid[robot.x][robot.y + 1], 0, -1);
                n.move(n.robot, 0, -1);
                neighbours.add(n);
            }
        }
        return neighbours;
    }

    private void move(Item item, int x, int y){
        itemGrid[item.x][item.y] = null;
        item.x += x;
        item.y += y;
        itemGrid[item.x][item.y] = item;
    }
}
