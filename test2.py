import numpy as np


x = np.array([(2, 3, 5, 6, 7, 3)], dtype=np.float32)
y = np.array([(5, 4, 6, 7, 8, 3)], dtype=np.float32)

x = x.ravel()
y=y.ravel()
a,b = np.polyfit(x, y, 1)

print(a, b)