import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

public class Test {
    public static void main(String[] args) {
        Map<Integer, Void> map = new HashMap<>();
        
                map.put(1, first());
                map.put(2, second());
                map.put(3, third());
            

        map.get(1);

    }

    public static Void first() {
        System.out.println("hi");
        return null;
    }

    public static Void second() {
        System.out.println("second");
        return null;
    }

    public static Void third() {
        System.out.println("third");
        return null;
    }
}
