# This code is in PYTHON2 and runs on the RPi

import cv2
import socket

debug = True


# Function run on quitting the script
def onquit():
    # Destroy the things which are no longer being used
    cap.release()
    cv2.destroyAllWindows()
    quit()


# Creates and binds to the socket used for communicating with the computer
commsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
commsocket.bind(('', 9001))

# Sets the maximum number of connections to 5
commsocket.listen(5)

# Waits and accepts the first one to attempt communication
graphicsconn, _ = commsocket.accept()

# Open Webcam
cap = cv2.VideoCapture(0)  # 0 signifies the first available camera device

# The protocol used for video
fourcc = cv2.cv.FOURCC(*"XVID")

while True:
    # Capture image from camera
    ret, frame = cap.read()
    # If the frame was captured correctly
    if ret:
        # Send the frame
        graphicsconn.send(bytearray(frame.flatten()))
        if debug:
            # Display it to the screen, for debugging
            cv2.imshow("frame", frame)
        # Wait, so it works
        cv2.waitKey(1)
