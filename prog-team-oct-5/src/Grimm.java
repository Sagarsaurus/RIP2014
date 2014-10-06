import java.util.Scanner;

public class Grimm {

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        int low = scan.nextInt(), high = scan.nextInt();
        while(low != 0){
            int[] factors = new int[high - low + 1];
            for(int i = low; i <= high; i++) {
                int num = i, max = -1;
                boolean found = false;
                for(int j = 2; j < num; j++){
                    if(num % j == 0) {
                        int k = 0;
                        for(; k < i - low; k++) {
                            if(factors[k] == j) {
                                max = k;
                                break;
                            }
                        }
                        if(k == i - low) {
                            factors[i - low] = j;
                            found = true;
                            System.out.print(j + " ");
                            break;
                        }
                        else {
                            num /= j;
                        }
                    }
                }
                if(!found) {
                    System.out.print(factors[max] + " ");
                }
            }
            low = scan.nextInt();
            high = scan.nextInt();
        }
    }
}
