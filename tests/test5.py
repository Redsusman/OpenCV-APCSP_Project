import cv2
import numpy as np

# create a numpy array
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.float32)

# convert the numpy array to an opencv cv::Mat object
mat = cv2.dnn.blobFromImage(arr, scalefactor=1.0, size=arr.shape, mean=(0, 0, 0), swapRB=False, crop=False)

secondMat = cv2.Mat(arr)
# print the cv::Mat object
print(type(mat))
print(type(arr))