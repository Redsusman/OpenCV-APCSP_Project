import cv2
import numpy as np
import cameraCalibration as calib


# used to control what color the camera should be looking, this interval can detect, say a purple cube.
# hopefully I can use a trained HaarCascadeClasifier xml for better tracking.
low = np.array([128, 50, 128])
high = np.array([255, 255, 255])
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

cubePointsInches = np.array([(0,0,0), (0, 9.5, 0), (9.5, 9.5, 0), (9.5, 0, 0)])
axis = np.float32([[0,0,0], [0,9.5,0], [9.5,9.5,0], [9.5,0,0],[0,0,-9.5],[0,9.5, -9.5],[9.5, 9.5,-9.5],[9.5,0,-9.5]])

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
    return distanceInches

def getPose(largest_contour):
    (x,y,w,h) = cv2.boundingRect(largest_contour)
    imagePoints = np.array([(x,y), (x, y+h), (x+w,y+h), (x+w, y)], dtype=np.float32)
    ret, rvec, tvec = cv2.solvePnP(cubePointsInches, imagePoints, mtx, dist, cv2.SOLVEPNP_ITERATIVE)
    rvec, _ = cv2.Rodrigues(rvec)
    return rvec, tvec

def drawBox(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    img = cv2.drawContours(img, [imgpts[:4]],-1,(0,255,0),-3)
    for i,j in zip(range(4),range(4,8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]),(255),3)
    img = cv2.drawContours(img, [imgpts[4:]],-1,(0,0,255),3)
    return img

def run():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
    # can use GaussianBlur function, but want to modify with matrix
        contrast = cv2.convertScaleAbs(frame, 0, 1.25)
        filter = cv2.GaussianBlur(contrast, (5,5), 0)
        convert = cv2.cvtColor(filter, cv2.COLOR_BGR2HSV)
        range = cv2.inRange(convert, low, high)
        range = cv2.morphologyEx(range, cv2.MORPH_OPEN, dilationKernel)
    # unused
        contours, _ = cv2.findContours(
            range, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for i in contours:
            (x, y, w, h) = cv2.boundingRect(i)
            if cv2.contourArea(i) > 150:
                cv2.rectangle(filter, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        if contours or len(contours) > 0:
            large_contour = max(contours, key=cv2.contourArea)
            pose = getPose(large_contour)
            cv2.putText(filter, str(pose[1]/2.54), (100, 100),
                    cv2.FONT_HERSHEY_COMPLEX, 0.25, (0, 255, 0), 1)
            imagePoints, jacobian = cv2.projectPoints(axis, pose[0], pose[1], mtx, dist)
            cv2.drawFrameAxes(filter, mtx, dist, pose[0], pose[1], 20, 10)
            drawBox(filter, axis, imagePoints)
            
        cv2.imshow("cube video", filter)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



