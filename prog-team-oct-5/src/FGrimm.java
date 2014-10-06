import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class FGrimm {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int low = scan.nextInt(), high = scan.nextInt();
        while(low != 0){
            grimm(low, high);
            low = scan.nextInt();
            high = scan.nextInt();
        }
    }
    public static void grimm(int low, int high) {
        List<Integer>[] primes = new ArrayList[high - low + 1];
        for(int i = 0; i <= high - low; i++){
            primes[i] = new ArrayList<Integer>();
        }
        List<Integer> hash = new ArrayList<Integer>();
        int sqrt = (int) Math.sqrt(high);
        for (int i = 2; i <= sqrt; i++) {
            boolean isP = true;
            for(int j: hash) {
                if(i % j == 0){
                    isP = false;
                    break;
                }
            }
            if(isP) {
                hash.add(i);
            }
        }
        for(int i = low; i <= high; i++) {
            for(int j: hash) {
                if(i % j == 0){
                    primes[i - low].add(j);
                }
            }
        }
        int[] indexes = new int[high - low + 1];
        for (int i = high - low; i >= 0 ; i--){
            for(int j = 0; j < i; j++);
        }
    }
}