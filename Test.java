import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

public class Test {
    public static void main(String[] args) {
        Thread loop = new Thread(() -> {
            for (int i = 0; i < 10; i++) {
                Thread secondLoop = new Thread(() -> {
                    for (int j = 0; j < 10; j++) {
                        System.out.println(j);
                        try {
                            Thread.sleep(10);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                });
                System.out.println(i);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                secondLoop.start();
            }
        });
        loop.start();
    }

}
