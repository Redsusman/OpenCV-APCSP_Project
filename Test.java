import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Test {

    static double[] list = {3, 4, 6 ,9,  3, 3, 3, 3, 3, 3};
    static double[][] dim = new double[3][3];
    static double[] copy = new double[list.length];


    public static void main(String args[]) {
     
      int index = 0;
      for(int i = 0; i < dim.length; i++) {

        for(int j = 0; j < dim[0].length; j++) {
          dim[i][j] = list[index++];
          System.out.println(index);
        }
      }
      // System.out.println(array);
      System.out.println(Arrays.deepToString(dim));
      System.out.print(dim);
    }

}
