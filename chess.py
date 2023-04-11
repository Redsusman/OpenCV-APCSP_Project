import cv2
import numpy as np

img = cv2.imread("OpenCV-APCSP_Project/assets/iloveimg-resized/IMG_0902.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, corners = cv2.findChessboardCorners(gray, (6,9), None)

cv2.drawChessboardCorners(img, (6,9), corners, ret)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
        





