import cv2
import numpy as np


cap = cv2.VideoCapture(0)
low = np.array([128, 50, 128])
high = np.array([255, 255, 255])


def getCoordinatesInches(contours):
    array = []
    for i in contours:
        moments = cv2.moments(i)
        if moments["m00"] != 0:
            center_x = int(moments["m10"]/moments["m00"])
            center_y = int(moments["m01"]/moments["m00"])
            array = [center_x/64, center_y/64]
            return array
    return array


while True:
    ret, frame = cap.read()
    convert = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    range = cv2.inRange(convert, low, high)
    ret, threshold = cv2.threshold(range, 150, 200, cv2.THRESH_BINARY)

    contours, hierarchies = cv2.findContours(
        range, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # cv2.drawContours(range, contours, -1, (255, 0, 0), 3)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 1000:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.putText(frame, str(getCoordinatesInches(contours)), (255, 255),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
