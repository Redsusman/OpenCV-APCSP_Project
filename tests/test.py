import numpy as np
import cv2

measurementMatrix = np.eye(3, dtype=np.float32)
transitionMatrix = np.array([[1, 0, 1, 0, 0, 0, 0, 0, 0],
                                               [0, 1, 0, 1, 0, 0, 0, 0, 0],
                                               [0, 0, 1, 0, 0, 0, 0, 0, 0],
                                               [0, 0, 0, 1, 0, 0, 0, 0, 0],
                                               [0, 0, 0, 0, 1, 0, 0, 0, 0],
                                               [0, 0, 0, 0, 0, 1, 0, 0, 0],
                                               [0, 0, 0, 0, 0, 0, 1, 0, 0],
                                               [0, 0, 0, 0, 0, 0, 0, 1, 0],
                                               [0, 0, 0, 0, 0, 0, 0, 0, 1]], dtype=np.float32)
    
    
processNoiseCov = np.eye(9, dtype=np.float32) * 1e-5
measurementNoiseCov = np.eye(3, dtype=np.float32) * 1e-1
errorCovPre = np.ones((3,3), dtype=np.float32)

temp2 = np.zeros((3,9), dtype=np.float32)

# temp2 = measurementMatrix * errorCovPre

temp3 = np.zeros((3,3), dtype=np.float32)

# newMat = cv2.gemm(temp2, measurementMatrix, 1, measurementNoiseCov, 1, temp3, cv2.GEMM_2_T)

temp4 = np.zeros((3, 9), dtype=np.float32)

temp5 = np.zeros((3,1), dtype=np.float32)

statePre = np.zeros((9,1), dtype=np.float32)

statePost = np.zeros((9,1), dtype=np.float32)

errorCovPost = np.zeros((9,9), dtype=np.float32)

temp2 = measurementMatrix * errorCovPre

mat = cv2.gemm(temp2, measurementMatrix, 1, measurementNoiseCov, 1, temp3, cv2.GEMM_2_T)

rvec_test = np.array([[30, 2, 5], [4, 32, 45], [24, 29, 3]], dtype=np.float32)


print(mat)
