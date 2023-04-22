import cv2
import numpy as np

# def getContourCorners(contours): 
#     for i in range(0, len(contours)-1):
#         corners = cv2.intersectConvexConvex(contours[i], contours[i+1])
#     if isinstance(corners, np.ndarray):
#         corners = corners.squeeze().tolist()
#     corners = [(int(corner[0]), int(corner[1])) for corner in corners]
#     return corners

img = cv2.imread("OpenCV-APCSP_Project/assets/conea.png")

low = np.array([0, 100, 200])
high = np.array([50, 255, 255])

convert = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
constraint = cv2.inRange(convert, low, high)
blur = cv2.GaussianBlur(constraint, (15, 15), 0)

edges = cv2.Canny(blur,50, 150)

contours, hierarchies = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for contour in contours:
    hull = cv2.convexHull(contour)


cv2.drawContours(img, hull, -1, (255, 0, 0), 3)




cv2.imshow("img", img)

cv2.waitKey(10000)
cv2.destroyAllWindows()
