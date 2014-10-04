package rip.hw1.planner;

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
    public State(String items[]){
        //TODO
    }
    public  State(State state){
        robot = new Item(state.robot);
        Item[] boxes = new Item[state.boxes.length];
        for(int i = 0; i < boxes.length; i++)
            boxes[i] = new Item(state.boxes[i]);
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
}
