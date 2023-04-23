import cv2
import numpy as np

# def getContourCorners(contours): 
#     for i in range(0, len(contours)-1):
#         corners = cv2.intersectConvexConvex(contours[i], contours[i+1])
#     if isinstance(corners, np.ndarray):
#         corners = corners.squeeze().tolist()
#     corners = [(int(corner[0]), int(corner[1])) for corner in corners]
#     return corners

img = cv2.imread("OpenCV-APCSP_Project/assets/cube.jpeg")
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
low = np.array([128, 50, 128])
high = np.array([255, 255, 255])

convert = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
constraint = cv2.inRange(convert, low, high)
blur = cv2.GaussianBlur(constraint, (5,5), 0)
blur = np.float32(blur)


# edges = cv2.Canny(blur,50, 150)
# edges = np.float32(edges)


# contours, hierarchies = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

corners = cv2.cornerHarris(blur, 2,3, 0.04)
corners = cv2.convertScaleAbs(corners)
contours, hierarchies = cv2.findContours(corners, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(img, contours, -1, (255, 0, 0), 1)


# cv2.drawContours(img, corners, -1, (255, 0, 0), 3)
cv2.imshow("img", img)

cv2.waitKey(10000)
cv2.destroyAllWindows()
