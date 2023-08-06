import java.util.Arrays;

public class Sort {
    public static void main(String[] args) {
        int[] list = {6, 0, 2, 5};
        System.out.println(Arrays.toString(sort(list)));
    }

    public static int[] sort(int[] array) {
        for(int i = 0; i < array.length; i++) {
            for(int j = i; j < array.length; j++) {
                if(array[i] > array[j]) {
                    array[i] = array[j];
                }
            }
        }

        return array;
    }

    
}
