import cv2
import numpy as np
import cameraCalibration as calib


# used to control what color the camera should be looking, this interval can detect, say a yellow cone.
# hopefully I can use a trained HaarCascadeClasifier xml for better tracking.
low = np.array([0, 100, 200])
high = np.array([50, 255, 255])
# used to blur images if camera gets too close to object, matrix computes weighed average of each pixel by matrix multiplication
# opencv tracks objects way better when image(s) are blurred
# according to https://en.wikipedia.org/wiki/Kernel_(image_processing)
# a 5*5 Gaussian matrix provides most blur
kernelMatrix = np.multiply(1/256, np.array([
    [1, 4, 6, 4, 1],
    [4, 16, 24, 16, 4],
    [6, 24, 36, 24, 6],
    [4, 16, 24, 16, 4],
    [1, 4, 6, 4, 1]]))


dilationKernel = np.ones((5, 5), np.uint8)

conePointsInches = np.array([(0, 0, 0), (4.1875, 0.25, 0), (
    8.375, 0.25, 0), (4.1875, 12.8125, 0)], dtype=np.float32)

mtx = calib.mtx
dist = calib.dist
tvecs = calib.tvecs
rvecs = calib.rvecs

# find the xy(later z) coordinates of an tracked object relative to the camera.


def getPose(contours):
    largest_contour = max(contours, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(largest_contour)
    imagePoints = np.array(
        [(x, y + h), ((x+w)/2, y+h), (x+w, y+h), ((x+w)/2, y)], dtype=np.float32)
    ret, rvec, tvec = cv2.solvePnP(
        conePointsInches, imagePoints, mtx, dist, cv2.SOLVEPNP_ITERATIVE)
    return rvec, tvec


def getContourCorners(contours):
    intersections = []
    if len(contours) > 1:
        for i in range(0, len(contours) - 1):
            corners = cv2.intersectConvexConvex(contours[i], contours[i+1])
            intersections.append(corners)

    return intersections


def run():
    cap = cv2.VideoCapture(0)
    # detecting yellow requires higher exposure
    cap.set(cv2.CAP_PROP_EXPOSURE, 0.5)
    while True:
        ret, frame = cap.read()
        exposure = cv2.convertScaleAbs(frame, dst=0, alpha=1.25)
    # can use GaussianBlur function, but want to modify with matrix
        filter = cv2.GaussianBlur(exposure, (5, 5), 0)
        convert = cv2.cvtColor(filter, cv2.COLOR_BGR2HSV)
        range = cv2.inRange(convert, low, high)
        range = cv2.morphologyEx(range, cv2.MORPH_OPEN, dilationKernel)
    # unused
        ret, threshold = cv2.threshold(range, 150, 200, cv2.THRESH_BINARY)

        contours, hierarchies = cv2.findContours(
            range, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for i in contours:
            (x, y, w, h) = cv2.boundingRect(i)
            if cv2.contourArea(i) > 175:
                cv2.rectangle(filter, (x, y), (x+w, y+h), (255, 0, 0), 2)

        if contours or len(contours) > 0:
            pose = getPose(contours)
            cv2.drawFrameAxes(filter, mtx, dist, pose[0], pose[1], 20, 10)
            cv2.putText(filter, str(pose[0]), (0, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
            print(pose[0])

        cv2.imshow("cone video", filter)
        # cv2.imshow("exposure", cv2.convertScaleAbs(filter, dst = 1.5, alpha=1.43))

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
