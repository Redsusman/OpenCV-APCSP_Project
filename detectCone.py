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


dilationKernel = np.ones((5,5), np.uint8)

mtx = calib.mtx
dist = calib.dist
tvecs = calib.tvecs
rvecs = calib.rvecs

# find the xy(later z) coordinates of an tracked object relative to the camera.
def getCoordinatesInches(contours):
    array = []
    for i in contours:
        moments = cv2.moments(i)
        if moments["m00"] != 0:
            center_x = int(moments["m10"]/moments["m00"])
            center_y = int(moments["m01"]/moments["m00"])
            center_distance = (center_y/64)/np.sin(np.radians(7))
            array = [center_x/64, center_y/64, center_distance]
            return array
    return array

def distance(objectDimensions, focalLength_mm, objectImageSensor):
    distanceInches = (objectDimensions * focalLength_mm/objectImageSensor)/25.4
    cv2.solvePnP()
    cv2.calibrateCamera()
    return distanceInches


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

        cv2.putText(filter, str(getCoordinatesInches(contours)), (0, 50),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

        cv2.imshow("cone video", filter)
        # cv2.imshow("exposure", cv2.convertScaleAbs(filter, dst = 1.5, alpha=1.43))

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def getPose(image):
    array = []
    objectPoints = np.array([getCoordinatesInches()[0], getCoordinatesInches()[1], getCoordinatesInches()[2]])
    contours, hierarchies = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in contours:
        (x,y) = cv2.boundingRect(i)
        array.append((x,y))

    ret, rvec, tvec = cv2.solvePnP(objectPoints, array, mtx, dist, cv2.SOLVEPNP_ITERATIVE)
    return np.array([rvec, tvec])