import java.util.*;

public class HTsunami {
    static class Node implements Comparable{
        int x, y;
        public Node(int x, int y){
            this.x = x;
            this.y = y;
        }

        @Override
        public int compareTo(Object o) {
            return y - ((Node)o).y;
        }

        public String toString(){
            return "(" + x + " " + y + ")";
        }
    }
    static class Edge {
        Node A, B;
        double distance;
        public Edge(Node A, Node B){
            this.A = A;
            this.B = B;
            distance = Math.sqrt(A.x*A.x+A.y*A.y);
        }

    }
    public static void Tsunami(Node[] cities){
        Arrays.sort(cities);
        System.out.println(Arrays.toString(cities));

        List<Node> visited = new ArrayList<Node>();
        visited.add(cities[0]);

        List<Node> line = new ArrayList<Node>();
        line.add(cities[1]);
        int y = cities[1].y;
        for(int i = 2; i < cities.length; i++){
            if(cities[i].y == y)
                line.add(cities[i]);
            else {
                Edge mine = null;
                double mind = 0;
                for(int j = 0; j < line.size(); j++){
                    Edge smalle = null;
                    double smalld = 0;
                    for (int k = 0; k < visited.size(); k++){
                        Edge e = new Edge(line.get(j), visited.get(k));
                        if(e.distance < smalld) {
                            smalld = e.distance;
                            smalle = e;
                        }
                    }
                    if(smalld < mind){
                        mind = smalld;
                        mine = smalle;
                    }
                }

            }
        }
    }
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int num;
        do {
            num = scan.nextInt();
            Node[] cities = new Node[num];
            for(int i = 0; i < num; i++){
                cities[i] = new Node(scan.nextInt(), scan.nextInt());
            }
            Tsunami(cities);
        } while(num != 0);
    }
}
