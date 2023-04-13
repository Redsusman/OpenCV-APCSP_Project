import cv2
import numpy as np
import cameraCalibration as calib

low = np.array([128, 50, 128])
high = np.array([255, 255, 255])
cubePointsInches = np.array([(0,0,0), (0, 9.5, 0), (9.5, 9.5, 0), (9.5, 0, 0)])

axis = np.float32([[0,0,0], [0,9.5,0], [9.5,9.5,0], [9.5,0,0],
                   [0,0,0],[0,0,0],[0,0,0],[0,0,0] ])

axisTwo = axis = np.float32([[0,0,0], [0,9.5,0], [9.5,9.5,0], [9.5,0,0],
                   [0,0,-9.5],[0,9.5, -9.5],[9.5, 9.5,-9.5],[9,5,0,-9.5] ])

mtx = calib.mtx
dist = calib.dist
tvecs = calib.tvecs
rvecs = calib.rvecs

def getPose(largest_contour):
    (x,y,w,h) = cv2.boundingRect(largest_contour)
    imagePoints = np.array([(x,y), (x, y+h), (x+w,y+h), (x+w, y)], dtype=np.float32)
    ret, rvec, tvec = cv2.solvePnP(cubePointsInches, imagePoints, mtx, dist, cv2.SOLVEPNP_ITERATIVE)
    rvec, _ = cv2.Rodrigues(rvec)
    return rvec, tvec

def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    # draw pillars in blue color
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
    return img
   

img = cv2.imread("OpenCV-APCSP_Project/assets/cube.jpeg")
convert = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(convert, low, high)

contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
large_contour = max(contours, key=cv2.contourArea)

(x, y, w, h) = cv2.boundingRect(large_contour)
cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),2)

pose = getPose(large_contour)
cv2.putText(img, str(getPose(large_contour)), (0, 10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)

imagePoints, jacobian = cv2.projectPoints(axis, pose[0], pose[1], mtx, dist)

cv2.drawFrameAxes(img, mtx, dist, pose[0], pose[1], 1, 10)

draw(img, axis, imagePoints)

cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()




