import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(
    "OpenCV-APCSP_Project/assets/haarcascade_frontalface_default.xml")

startpoint = (5, 5)
color = (255, 0, 0)
CENTER = (255, 255)


def getAngle(img):
    return (x, y)


while True:

    ret,  frame = cap.read()
    cv2.putText(frame, "hello world", (255, 255),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1)
    convert = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(convert, 1.1, 4)

    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x+w, y + h), (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
