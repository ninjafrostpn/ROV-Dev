# This code is in PYTHON2 and runs on the RPi

import cv2
import socket

# Creates and binds to the socket used for communicating with the computer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 9001))

# Sets the maximum number of connections to 5
s.listen(5)

# Waits and accepts the first one to attempt communication
conn, addr = s.accept()

# Open Webcam
cap = cv2.VideoCapture(0)  # 0 signifies the first available camera device

# The protocol used for video
fourcc = cv2.cv.FOURCC(*"XVID")

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

# Destroy the things which are no longer being used
cap.release()
cv2.destroyAllWindows()
