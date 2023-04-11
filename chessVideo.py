import cv2
import numpy as np

cap = cv2.VideoCapture(0)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, (6,9), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

    if ret == True:
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1, -1), criteria)
        cv2.drawChessboardCorners(frame, (6,9), corners2, ret)
    
    cv2.imshow("img", frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()




