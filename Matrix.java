import java.io.IOException;
import java.lang.ProcessBuilder.Redirect.Type;
import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeSet;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.IntFunction;
import java.util.function.ToDoubleFunction;
import java.util.stream.Collector;
import java.util.stream.Collectors;

public class Matrix {

    public double[][] baseMatrix;
    public int rows;
    public int columns;

    public Matrix(int rows, int columns) {
        this.rows = rows;
        this.columns = columns;
        double[][] matrix = new double[rows][columns];
        baseMatrix = matrix;
    }

    /**
     * 
     * @return number of rows in instantiated Matrix object.
     */
    public int getRows() {
        return rows;
    }

    /**
     * 
     * @return number of columns in instantiated Matrix object.
     */
    public int getColumns() {
        return columns;
    }

    /**
     * 
     * @return get the base matrix/multidimensional a array the Matrix object uses
     */
    public double[][] getBaseMatrix() {
        return baseMatrix;
    }

    /**
     * populate a empty matrix with a list of values, by 1d array. The different
     * shapes between the list and matrix will be automatically handled by this
     * function
     * 
     * @param matrix
     * @param list
     */
    public void fill(Matrix matrix, double[] list) throws IOException {
        if (list.length - 1 < matrix.rows * matrix.columns) {
            int index = 0;
            for (int i = 0; i < matrix.rows; i++) {
                for (int j = 0; j < matrix.columns; j++) {
                    matrix.baseMatrix[i][j] = list[index++];
                    if (index >= list.length) {
                        matrix.baseMatrix[i][j] = list[list.length - 1];
                        index = list.length - 1;
                        list[index] = 0;
                        // list[list.length - 1] = 0;
                    }
                }
            }
        } else {
            throw new IOException("cannot fill this matrix with uneven values to rows and columns");
        }
    }

    /**
     * 
     * @param list
     * @param rows
     * @param columns
     * @return a constructed matrix with rows*columns shape, with values in matrix
     *         filled by 1d array.
     * @throws IOException
     */
    public static Matrix createMatrix(double[] list, int rows, int columns) throws IOException {
        Matrix ret = new Matrix(rows, columns);
        ret.fill(ret, list);
        return ret;
    }

    /**
     * 
     * @param rows
     * @param columns
     * @return a constructed/empty default matrix with specified rows*columns shape.
     */
    public static Matrix createEmptyMatrix(int rows, int columns) {
        Matrix ret = new Matrix(rows, columns);
        return ret;
    }

    /**
     * 
     * @param list
     * @return a Matrix object with the baseMatrix being the inputed dimensional
     *         list
     */
    public static Matrix createMatrixFromList(double[][] list) {
        Matrix ret = new Matrix(list.length, list[0].length);
        ret.baseMatrix = list;
        return ret;
    }

    public static Matrix createMatrix1dArray(double[] list) {
        Matrix ret = new Matrix(1, list.length);
        for (int i = 0; i < list.length; i++) {
            ret.baseMatrix[0][i] = list[i];
        }
        return ret;
    }

    /**
     * 
     * @param base
     * @param other
     * @return the sum/addition between two matrices.
     * @throws IOException if the shape of both matrices don't match.
     */
    public Matrix add(Matrix base, Matrix other) throws IOException {
        Matrix sum = new Matrix(base.rows, base.columns);
        if ((base.rows == other.rows) && (base.columns == other.columns)) {
            for (int i = 0; i < base.rows; i++) {
                for (int j = 0; j < base.columns; j++) {
                    sum.baseMatrix[i][j] = base.baseMatrix[i][j] + other.baseMatrix[i][j];
                }
            }
        } else {
            throw new IOException("must have same number of rows and columns for matrices");
        }

        return sum;
    }

    /**
     * 
     * @param base
     * @param other
     * @return the difference/subtraction between two matrices.
     * @throws IOException if the shapes of both inputed matrices don't match.
     */
    public Matrix subtract(Matrix base, Matrix other) throws IOException {
        Matrix difference = new Matrix(base.rows, base.columns);
        if ((base.rows == other.rows) && (base.columns == other.columns)) {
            for (int i = 0; i < base.rows; i++) {
                for (int j = 0; j < base.columns; j++) {
                    difference.baseMatrix[i][j] = base.baseMatrix[i][j] - other.baseMatrix[i][j];
                }
            }
        } else {
            throw new IOException("must have same number of rows and columns for matrices");
        }

        return difference;
    }

    /**
     * reconstructs a matrix with a different shape. I.e: convert a 6*2 matrix into
     * a 3*4 matrix, the reshape rows and columns should be multiples of the
     * original matrix, or equals
     * the product between the rows and columns of the original matrix, i.e,
     * reconstructing a 3*4
     * to a 6*2 matrix works because 3*4, and 6*2 = 12.
     * 
     * @param matrix
     * @param length
     * @throws IOException if shapes aren't compatible to change.
     */
    public Matrix reshape(Matrix matrix, int rows, int columns) throws IOException {
        Matrix blank = new Matrix(rows, columns);
        try {
            if (rows * columns == matrix.rows * matrix.columns) {
                double[] unravel = Matrix.unravel(matrix.baseMatrix);
                int index = 0;
                for (int i = 0; i < blank.rows; i++) {
                    for (int j = 0; j < blank.columns; j++) {
                        blank.baseMatrix[i][j] = unravel[index++];
                    }
                }
            } else {
                throw new IOException("reshape isn't compatible with current shape");
            }
            return blank;
        } catch (IndexOutOfBoundsException e) {
            System.out.println("reshape isn't compatible with current shape");
            return null;
        }
    }

    /**
     * 
     * @param n number to specify the rows, or columns, doesn't matter both will
     *          form a square n*n.
     * @return a square matrix with 1's filling the diagonals only, and the rest
     *         with 0's.
     */
    public static Matrix eye(int n) {
        Matrix eye = new Matrix(n, n);
        for (int i = 0; i < n; i++) {
            eye.baseMatrix[i][i] = 1;
        }
        return eye;
    }

    /**
     * 
     * @param matrix
     * @param other
     * @return product/multiplication between two matrices.
     * @throws IOException
     */
    public Matrix dot(Matrix matrix, Matrix other) throws IOException {
        Matrix ret = new Matrix(matrix.rows, matrix.columns);
        if (matrix.columns == other.rows) {
            for (int i = 0; i < matrix.rows; i++) {
                for (int j = 0; j < matrix.columns; j++) {
                    for (int k = 0; k < other.columns; k++) {
                        ret.baseMatrix[i][j] += matrix.baseMatrix[i][k] * other.baseMatrix[k][j];
                    }
                }
            }
            return ret;
        } else {
            throw new IOException("Matrix A columns must be the same number of rows from Matrix B");
        }
    }

    /**
     * 
     * @param matrix
     * @param constant
     * @return a matrix with all values multiplied/scaled by a single numerical
     *         constant, useful if not multiplying by another matrix.
     */
    public Matrix scale(Matrix matrix, double constant) {
        for (int i = 0; i < matrix.rows; i++) {
            for (int j = 0; j < matrix.columns; j++) {
                matrix.baseMatrix[i][j] *= constant;
            }
        }
        return matrix;
    }

    /**
     * 
     * @param matrix
     * @param other
     * @return division between two matrices
     * @throws IOException if Matrix A doesn't have the same number of rows as
     *                     Matrix B.
     */
    public Matrix divide(Matrix matrix, Matrix other) throws IOException {
        Matrix ret = new Matrix(matrix.rows, matrix.columns);
        if (matrix.columns == other.rows) {
            for (int i = 0; i < matrix.rows; i++) {
                for (int j = 0; j < matrix.columns; j++) {
                    for (int k = 0; k < other.columns; k++) {
                        ret.baseMatrix[i][j] += matrix.baseMatrix[i][k] / other.baseMatrix[k][j];
                    }
                }
            }
            return ret;
        } else {
            throw new IOException("Matrix A columns must be the same number of rows from Matrix B");
        }
    }

    /**
     * 
     * @param matrix
     * @return returns a matrix, with the column values as the row values, and vice
     *         versa.
     */
    public Matrix transpose(Matrix matrix) {
        Matrix ret = new Matrix(matrix.getColumns(), matrix.getRows());
        for (int i = 0; i < matrix.columns; i++) {
            for (int j = 0; j < matrix.rows; j++) {
                ret.baseMatrix[i][j] = matrix.baseMatrix[j][i];
            }
        }
        return ret;
    }

    /**
     * 
     * @param matrix
     * @return get the determinant, or the difference between the cross-products of
     *         the two diagonals of a matrix
     * @throws IOException if the matrix doesn't have square dimensions, i.e: (2*2),
     *                     (3*3), not (3*2)
     */
    public double determinant(Matrix matrix) throws IOException {

        if (matrix.rows == matrix.columns) {
            double ret = 0;
            double diagonalProduct = 1;
            double secondDiagonalProduct = 1;
            for (int i = 0; i < matrix.getColumns(); i++) {
                diagonalProduct *= matrix.baseMatrix[i][i];

            }
            for (int i = 0, j = matrix.baseMatrix[0].length - 1; i < matrix.baseMatrix.length && j >= 0; i++, j--) {
                secondDiagonalProduct *= matrix.baseMatrix[i][j];

            }
            ret = diagonalProduct - secondDiagonalProduct;
            return ret;
        } else {
            throw new IOException("must be a square matrix, i.e: (1*1), (2*2), (3*3)...");
        }
    }

    public double determinantLargerValue() {
        return 2;
    }

    public static double[] unravel(double[][] dimensionalArray) {
        int c = 0;
        double[] unravel = new double[dimensionalArray.length * dimensionalArray[0].length];
        for (int i = 0; i < dimensionalArray.length; i++) {
            for (int j = 0; j < dimensionalArray[0].length; j++) {
                unravel[c++] = dimensionalArray[i][j];
            }
        }
        return unravel;
    }

    /**
     * 
     * @param rows
     * @param columns
     * @param constant
     * @return create a x*y matrix, with all values filled with the inputed
     *         constant,
     *         example: rows = 3, columns = 2, constant = 4 creates a 3*2 matrix
     *         filled with 4's
     */
    public static Matrix constantMatrix(int rows, int columns, double constant) {
        Matrix ret = new Matrix(rows, columns);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                ret.baseMatrix[i][j] = constant;
            }
        }
        return ret;
    }

    public static Matrix randomMatrix(int rows, int columns, int[] range, boolean roundVal) {
        Matrix ret = new Matrix(rows, columns);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < columns; j++) {
                double randomVal = Math.random() * (range[1] - range[0]) + range[0];
                randomVal = roundVal ? (int) Math.round(randomVal) : randomVal;
                ret.baseMatrix[i][j] = randomVal;
            }
        }
        return ret;
    }

    public ArrayList<Matrix> cofactor(Matrix matrix) throws IOException {

        ArrayList<Matrix> storedPossibilites = new ArrayList<>();
        int rowCheck = 0;
        int rowChecker = matrix.rows - rowCheck;

        for (int i = 0; i < matrix.rows; i++) {
            rowCheck++;
            for (int j = 0; j < matrix.columns; j++) {
                Matrix possibility = new Matrix(matrix.rows - 1, matrix.columns - 1);
                ArrayList<Double> list = new ArrayList<>();
                if ((matrix.baseMatrix[i][j] != matrix.baseMatrix[0][j])
                        && (matrix.baseMatrix[i][j] != matrix.baseMatrix[i][i])) {
                    list.add(matrix.baseMatrix[i][j]);
                    double[] doubleList = list.stream().mapToDouble(Double::doubleValue).toArray();
                    possibility.fill(possibility, doubleList);
                }
                storedPossibilites.add(possibility);
                if (storedPossibilites.get(storedPossibilites.size() - 1).rows != 2) {
                    for (Matrix possibilit : storedPossibilites) {
                        if (possibilit.rows == rowChecker) {
                            return cofactor(possibilit);
                        } else if (rowChecker == 0) {
                            break;

                        }
                    }
                }
            }

        }

        return storedPossibilites;
    }

    /**
     * 
     * @param matrix
     * @return the inverse of a matrix
     * @throws IOException if matrix isn't square.
     */
    public Matrix inverse(Matrix matrix) throws IOException {
        double inverseCoefficent = 1 / determinant(matrix);
        Matrix diagonalMatrix = adjugate(matrix);
        Matrix inverseMatrix = diagonalMatrix.scale(diagonalMatrix, inverseCoefficent);
        return inverseMatrix;
    }

    public Matrix factor(Matrix matrix) {
        Matrix ret = new Matrix(matrix.rows, matrix.columns);

        for (int i = 0; i < matrix.rows; i++) {
            for (int j = 0; j < matrix.columns; j++) {
                if (matrix.baseMatrix[0][i] == matrix.baseMatrix[0][j]) {
                    continue;
                }

                ret.baseMatrix[i][j] = matrix.baseMatrix[i][j];
                System.out.println(ret.baseMatrix[i][j]);
            }
        }

        return ret;

    }

    /**
     * 
     * @param matrix
     * @return a matrix with diagonals as rows of numbers.
     */
    public Matrix adjugate(Matrix matrix) {
        Matrix ret = new Matrix(matrix.getRows(), matrix.getColumns());
        for (int i = 0, j = matrix.getColumns() - 1; i < matrix.getColumns() && j >= 0; i++, j--) {
            for (int k = 0, o = k + 1; k < matrix.getRows() && o < matrix.getRows(); k++, o++) {
                ret.baseMatrix[j][i] = matrix.baseMatrix[j][i] * -1;
                ret.baseMatrix[i][i] = matrix.baseMatrix[j][j];
            }
        }
        return ret;
    }

    /**
     * 
     * @param function         elementary function, with f(x)dx being continous on
     *                         the interval.
     *                         basic syntax: Function<Double, Double> ret = x ->
     *                         .... ex: Math.sin(x) + 2*x
     * @param interval         interval of two x points, i.e [1, 3];
     * @param linspaceInterval length/step of each reiman rectangle on the
     *                         x-axis-interval, such
     *                         as 0.002 or 1.
     * @return the approximated definite integral, for a better approximation,
     *         reduce the linespaceInterval number closer to 0, however this will
     *         slow down execution if too low of linspace.
     */
    public static double reimanSumIntegral(Function<Double, Double> function, int[] interval, double linspaceInterval) {

        List<Double> intervalList = new LinkedList<>();
        for (double i = interval[0]; i <= interval[1]; i += linspaceInterval) {
            intervalList.add(i);
        }
        double sum = 0;
        try {
            for (var x : intervalList) {
                double y = function.apply(x);
                if (!Double.isNaN(y)) {
                    sum += linspaceInterval * y;
                } else {
                    throw new RuntimeException(
                            y + "invalid interval, a jump, infinite, or other discontinouty invalidates this interval, use a continous interval");
                }
            }
        } catch (ArithmeticException e) {
            System.out.println(e + "invald interval, some kind of discontinuity in the function");
        }
        return sum;
    }

    /**
     * 
     * @param function
     * @param x        point to be evaluated
     * @param h        width of slope, set closer to 0. For small number notation,
     *                 use 1E-n notation
     * @return derivative (d/dx with respect to f(x)) calculated by the difference
     *         quotient: (f(x+h) - f(x))/h
     */
    public static double derivative(Function<Double, Double> function, double x, double h) {
        double retDerivative = (function.apply(x + h) - function.apply(x)) / h;
        return retDerivative;
    }

    private static double newton(Function<Double, Double> function, double x) {
        double approx = x - (function.apply(x) / derivative(function, x, 1E-10));
        return approx;
    }

    private static double newtonZero(Function<Double, Double> function, double x) {
        do {
            x = newton(function, x);
        } while (Math.abs(function.apply(x)) > 1E-10);
        return x;
    }

    private static void cleanZeros(ArrayList<Double> possibleZeros) throws InterruptedException {

        ArrayList<Double> synchronizedPossibleZeros = new ArrayList<>(Collections.synchronizedList(possibleZeros));
    
        Thread thread = new Thread(() -> {
            Map<Integer, List<String>> groupedZeros = Collections.synchronizedMap(new HashMap<>());
            List<String> strList = Collections.synchronizedList(new ArrayList<>());
            synchronizedPossibleZeros.forEach(number -> strList.add(Double.toString(number)));
            for (int i = 0; i < synchronizedPossibleZeros.size() - 1; i++) {
                final int currentIndex = i; // Capture the current index as a final variable
                Thread secondLoop = new Thread(() -> {
                    for (int j = 0; j < 4; j++) {
                        if (Character.compare(strList.get(currentIndex).charAt(j), strList.get(currentIndex + 1).charAt(j)) == 0) {
                            int arrayCount = 0;
                            System.out.println(arrayCount);
                            arrayCount++;
                            synchronized (groupedZeros) {
                                groupedZeros.put(arrayCount, new ArrayList<String>());
                                groupedZeros.get(arrayCount).add(strList.get(currentIndex));
                                groupedZeros.get(arrayCount).add(strList.get(currentIndex + 1));
                            }
                            break;
                        }
                        try {
                            Thread.sleep(10);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                });
                secondLoop.start();
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            groupedZeros.forEach(
                    (a, b) -> b.stream().mapToDouble(Double::parseDouble).boxed().collect(Collectors.toList()));
                    System.out.println(groupedZeros);
        });
        thread.start();

    
        thread.join();
    }

    /**
     * 
     * @param function nth degree polynomial.
     * @return zeros approximated by the Newton-Rasphon method.
     */
    public static ArrayList<Double> zeros(Function<Double, Double> function) {
        ArrayList<Double> xList = new ArrayList<>();
        ArrayList<Double> approxRoots = new ArrayList<>();

        for (double i = -100; i < 100; i++) {
            double y = function.apply(i);
            if (Math.signum(y) != Math.signum(function.apply(i + 1))) {
                xList.add(i);
                xList.add(i + 1);
            }
        }
        for (var x : xList) {
            approxRoots.add(newtonZero(function, x));
        }
        // filter system for set of "solutions";
        approxRoots.removeIf(x -> Math.abs(x) < 0.001 && function.apply(x) != 0.0 || Double.isNaN(x)
                || Double.isInfinite(x) || Math.abs(function.apply(x)) > 1 || Double.isNaN(function.apply(x))
                || Double.isInfinite(function.apply(x)));

        List<String> strList = new ArrayList<String>();
        approxRoots.forEach(number -> strList.add(Double.toString(number)));
        // hashsets remove/filter double solutions
        Set<Double> convertApprox = new HashSet<>();
        convertApprox.addAll(approxRoots);
        ArrayList<Double> reconvert = new ArrayList<>(convertApprox);
        Collections.sort(reconvert);
        return reconvert;
    }

    public double[] regression(double[] xList, double[] yList, int power) {
        double[] retCoefficents = new double[power];
        return retCoefficents;
    }

    public static void main(String[] args) throws IOException {
        // 4x^4 - 9x^3 + 2x^2 - 8x + 3

        ArrayList<Double> list = new ArrayList<>() {
            {
                add(1.7771);
                add(1.7772);
                add(2.7772);
                add(2.77771);

            }
        };

        try {
            cleanZeros(list);
        } catch (InterruptedException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

}