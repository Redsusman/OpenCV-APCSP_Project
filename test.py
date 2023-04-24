import numpy as np
import numpy.linalg as lin

array = np.zeros((9,3), dtype=np.float32)
arrayTwo = np.eye(3, dtype=np.float32)

print(np.dot(array, arrayTwo))