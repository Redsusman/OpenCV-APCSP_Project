import numpy as np

array = np.array([[3, 5, 1], [4, 5, 2],[9, 8, 4]], dtype=np.float32)
array = array.reshape(-1, 3)

print(array)