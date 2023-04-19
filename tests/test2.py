import numpy as np
import cv2

rot_matrix = np.array([[0.99810947, -0.06146124,  0.00747026],
                       [0.06149522,  0.99804294, -0.01432203],
                       [-0.00699179,  0.01443818,  0.9998746]], dtype=np.float32)

rot_vector, _ = cv2.Rodrigues(rot_matrix)

print(rot_vector.shape)