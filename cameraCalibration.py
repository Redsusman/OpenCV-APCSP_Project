# credit to https://learnopencv.com/camera-calibration-using-opencv/
# https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
import cv2
import numpy as np
import os
import glob

Checkerboard = (6, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((Checkerboard[0] * Checkerboard[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:Checkerboard[0], 0:Checkerboard[1]].T.reshape(-1, 2)

objectPoints = []
imagePoints = []

gray = None


files = glob.glob("./OpenCV-APCSP_Project/assets/iloveimg-resized/*.png")

for file in files:
    img = cv2.imread(file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(
        gray, Checkerboard, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    if ret == True:
        objectPoints.append(objp)
        cornersTwo = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criteria)
        imagePoints.append(cornersTwo)

cv2.destroyAllWindows()


ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objectPoints, imagePoints, gray.shape[::-1], None, None)


def getProjectionError():
    mean_error = 0
    for i in range(len(objectPoints)):
        imgpoints2, _ = cv2.projectPoints(
            objectPoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imagePoints[i], imgpoints2,
                         cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
    print("total error: {}".format(mean_error/len(objectPoints)))


# ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objectPoints, imagePoints, gray.shape[::-1], None, None)

# print(mtx)
# print(dist)
# print(rvecs)
# print(tvecs)
