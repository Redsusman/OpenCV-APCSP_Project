import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class New {
    public static void main(String[] args) throws IOException {
        int[] array = { 2, 3, 5, 6, 7, 8, 9 };
        toTxtFile(array);
    }
 
    public static File toTxtFile(int[] array) throws IOException {
        File ret = new File("ret.txt");
        FileWriter writer = new FileWriter(ret);
        writer.write("[");
            for (int number : array) {
            writer.write(Integer.toString(number) + ",\n");
        }
        writer.write("]");
        writer.close();
        return ret;
    }

    // public static File arrayFile
}
