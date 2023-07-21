import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

public class Test {
    public static void main(String[] args) throws IOException {
        File file = new File("file.csv");
        file.createNewFile();

        ArrayList<String[]> dataStream = new ArrayList<>() {{
            add(new String[] {"John", "Doe", "1987"});
            add(new String[] {"Mary", "Rose", "1942"});
            add(new String[] {"John", "Clark", "2012"});
        }};

        try (PrintWriter writer = new PrintWriter(file)) {
            for (String[] data : dataStream) {
                StringBuilder line = new StringBuilder();
                for (int i = 0; i < data.length; i++) {
                    line.append(data[i]);
                    if (i < data.length - 1) {
                        line.append(",");
                    }
                }
                writer.write(line.toString() + "\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
