import cv2
import numpy as np

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")




while True:
    
    _,  frame = cap.read()
    convert = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(convert, 1.1, 4)

    for(x, y, z, c,) in face:
        cv2.rectangle(frame, x, c, (0, 255, 0), 1.1, -1, 0)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
    






