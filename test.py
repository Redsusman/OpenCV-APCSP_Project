import numpy as np

x_list = np.array([30, 35, 50, 70, 90], dtype=np.float32)
y_list = np.array([5, 5, 3.6, 3.6, 1.4], dtype=np.float32)

a, b, c = np.polyfit(x_list, y_list, 2)

print(a, b, c)