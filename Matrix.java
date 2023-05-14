import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

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
     * shapes between the list and matrix will automatically handled by this
     * function
     * 
     * @param matrix
     * @param list
     */
    public void fill(Matrix matrix, double[] list) {
        for (int i = 0; i < matrix.rows; i++) {
            for (int j = 0; j < matrix.columns; j++) {
                matrix.baseMatrix[i][j] = list[j];
            }
        }
    }

    /**
     * 
     * @param list
     * @param rows
     * @param columns
     * @return a constructed matrix with rows*columns shape, with values in matrix
     *         filled by 1d array.
     */
    public static Matrix createMatrix(double[] list, int rows, int columns) {
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
     */
    public Matrix reshape(Matrix matrix, int rows, int columns) throws IndexOutOfBoundsException {
        
        Matrix blank = new Matrix(rows, columns);
        double[] unravel = Matrix.unravel(matrix.baseMatrix);
        int index = 0;
        for (int i = 0; i < blank.rows; i++) {
            for (int j = 0; j < blank.columns; j++) {
                blank.baseMatrix[i][j] = unravel[index++];
            }
        }
        return blank;
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
     *         constant, useful if not multuplying by another matrix.
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

    public static void main(String[] args) throws IOException {
        double[][] list = { { 1, 2 }, { 3, 4 }, { 5, 3 }, { 5, 6 }, { 9, 3 }, { 10, 4 } };
        Matrix matrix = Matrix.createMatrixFromList(list);
        Matrix reshape = matrix.reshape(matrix, 4, 3);
        System.out.println(Arrays.deepToString(reshape.baseMatrix));
    }

}