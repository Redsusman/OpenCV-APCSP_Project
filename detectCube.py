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

cubePointsInches = np.array(
    [(0, 0, 0), (0, 9.5, 0), (9.5, 9.5, 0), (9.5, 0, 0)])
axis = np.float32([[0, 0, 0], [0, 9.5, 0], [9.5, 9.5, 0], [9.5, 0, 0], [
                  0, 0, -9.5], [0, 9.5, -9.5], [9.5, 9.5, -9.5], [9.5, 0, -9.5]])

dilationKernel = np.ones((5, 5), np.uint8)

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


def getPose(contours):
    largest_contour = max(contours, key=cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(largest_contour)
    imagePoints = np.array(
        [(x, y), (x, y+h), (x+w, y+h), (x+w, y)], dtype=np.float32)
    ret, rvec, tvec, inliers = cv2.solvePnPRansac(
        cubePointsInches, imagePoints, mtx, dist, iterationsCount=1000, reprojectionError=2.00, confidence=0.9)
    rvec2, tvec2 = cv2.solvePnPRefineLM(
        cubePointsInches, imagePoints, mtx, dist, rvec, tvec)
    rvec2, _ = cv2.Rodrigues(rvec2)
    return rvec2, tvec2, inliers


def drawBox(img, corners, imgpts, color):
    imgpts = np.int32(imgpts).reshape(-1, 2)
    img = cv2.drawContours(img, [imgpts[:4]], -1, color, -3)
    for i, j in zip(range(4), range(4, 8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), color, 3)
    img = cv2.drawContours(img, [imgpts[4:]], -1, color, 3)
    return img


def run():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
    # can use GaussianBlur function, but want to modify with matrix
        contrast = cv2.convertScaleAbs(frame, 0, 1.25)
        filter = cv2.GaussianBlur(contrast, (11, 11), 0)
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
            pose = getPose(contours)

            cv2.putText(filter, str(pose[1]), (50, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 0.25, (0, 255, 0), 1)
            cv2.putText(filter, str([np.degrees(angle) for angle in pose[0]]), (50, 200),
                        cv2.FONT_HERSHEY_COMPLEX, 0.25, (0, 255, 0), 1)

            secondImagePoints, jacobian = cv2.projectPoints(
                axis, correctRotation(pose[0], pose[1], cap, pose[2], 2)[2], pose[1], mtx, dist)

            cv2.drawFrameAxes(filter, mtx, dist, pose[0], pose[1], 20, 10)
            drawBox(filter, axis, secondImagePoints, (0, 0, 255))
            # print(str([np.degrees(angle) for angle in secondPose[1]]))
        cv2.imshow("cube video", filter)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# correct for wrong rotation brought on by limitations of perspective n'perspective model (flipped rvec signs)


def correctRotation(measurement, tvec, cap, poseInliers, minKalmanInliers):

    kalman_filter = cv2.KalmanFilter(9, 3, 0)
    if cap.isOpened():
        dt = cap.get(cv2.CAP_PROP_POS_MSEC)/1000
        if not cap.isOpened():
            dt = 0.01
    if (measurement.shape == (3, 3)) or (poseInliers.shape[0] >= minKalmanInliers):
        measurement, _ = cv2.Rodrigues(measurement)
        measurement = measurement.astype(np.float32)
        measurementMatrix = np.eye(3, 9, dtype=np.float32)
        transitionMatrix = np.array([[1, 0, 0, dt, 0, 0, 0, 0, 0],
                                     [0, 1, 0, 0, dt, 0, 0, 0, 0],
                                     [0, 0, 1, 0, 0, dt, 0, 0, 0],
                                     [0, 0, 0, 1, 0, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 1, 0, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 1, 0, 0, 0],
                                     [0, 0, 0, 0, 0, 0, 1, dt, 0],
                                     [0, 0, 0, 0, 0, 0, 0, 1, dt],
                                     [0, 0, 0, 0, 0, 0, 0, 0, 1]], dtype=np.float32)

        processNoiseCov = np.eye(9, dtype=np.float32) * 1e-6
        measurementNoiseCov = np.eye(3, dtype=np.float32) * 1e-3
        errorCovPre = np.ones((9, 9), dtype=np.float32)
        statePre = np.zeros((9, 1), dtype=np.float32)
        errorCovPost = np.zeros((9, 9), dtype=np.float32)
        statePost = np.zeros((9, 1), dtype=np.float32)

        kalman_filter.measurementMatrix = measurementMatrix
        kalman_filter.transitionMatrix = transitionMatrix
        kalman_filter.processNoiseCov = processNoiseCov
        kalman_filter.measurementNoiseCov = measurementNoiseCov
        kalman_filter.errorCovPre = errorCovPre
        kalman_filter.errorCovPost = errorCovPost
        kalman_filter.statePre = statePre
        kalman_filter.statePost = statePost

        dot_product = np.dot(kalman_filter.statePre[:3].T, measurement)

        if dot_product < 0:
            measurement *= -1

        for _ in range(1000):
            prediction = kalman_filter.predict()
            kalman_filter.correct(measurement)
            estimate = kalman_filter.correct(measurement)

        final_estimate = prediction[:3, :3]
        final_estimate = final_estimate.astype(type(tvec[0][0]))

        # prediction = kalman_filter.predict()
        # kalman_filter.correct(measurement)
        # prediction = kalman_filter.predict()
        second_final_estimate = kalman_filter.statePost[:3, :3]
        second_final_estimate = second_final_estimate.astype(type(tvec[0][0]))

        third_final_estimate = estimate[:3, :3]
        # third_final_estimate = cv2.Rodrigues(third_final_estimate)

        # third_final_estimate = estimate.astype(type(tvec[0][0]))
        return final_estimate, second_final_estimate, third_final_estimate
