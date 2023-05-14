import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Test {

    


    public static void main(String args[]) {
      System.out.println(cofactorPossible(5));
    }

    public static double cofactorPossible(int rows) {
      double first = 1;
      double sum = 1;
      for(int i = rows; i >= 2; i--) {
        first = sum * (i-1) * i;
        sum += first;
        System.out.println(sum);
      }
      return sum;
    }

}
