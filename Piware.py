# This code is in PYTHON2 and runs on the RPi

import cv2
import socket
import threading
import numpy as np
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 9001))
s.listen(5)
conn, addr = s.accept()

# Open Webcam
cap = cv2.VideoCapture(0)  # 1 signifies the second available camera device
fourcc = cv2.cv.FOURCC(*"XVID")  # The protocol used for video

camon = True
while camon:
    # Capture image from camera
    ret, frame = cap.read()
    # If the frame was captured correctly
    if ret:
        # print(frame.dtype, frame.shape)
        conn.send(bytearray(frame.flatten()))
        cv2.imshow("frame", frame)
        cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
