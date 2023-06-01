import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Test {

    public static void main(String args[]) throws IOException {
        double[] list = { 3, 4, 5, 3, 1, 2, 7, 8, 3 };
        Matrix m = Matrix.createMatrix(list, 3, 3);
        Matrix newMat = new Matrix(m.rows, m.columns);
        ArrayList<Matrix> arrays = new ArrayList<>();

        for (int i = 0; i < m.rows; i++) {
            Matrix matrix = new Matrix(m.rows, m.columns);
            for (int j = 0; j < m.columns; j++) {
                if ((m.baseMatrix[i][i] != m.baseMatrix[0][j]) && (m.baseMatrix[i][j] != m.baseMatrix[i][0])) {

                    matrix.baseMatrix[i][j] = m.baseMatrix[i][j];
                    arrays.add(matrix);
                    // newMat.baseMatrix[i][j] = m.baseMatrix[i][j];

                }
            }
        }

        for (Matrix mat : arrays) {
            System.out.println(Arrays.deepToString(mat.baseMatrix));
        }
    }

}
