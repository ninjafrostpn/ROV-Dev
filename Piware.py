# This code is in PYTHON2 and runs on the RPi

import cv2
import socket
import threading

debug = True

# Options for command 3-bit command code (PLS NOTE: MUST BE THE SAME IN THE COMP CODE)
TYPE_OPTIONS = 0
TYPE_MOTOR_1 = 1
TYPE_MOTOR_2 = 2
TYPE_MOTOR_3 = 3
TYPE_LIGHTS = 4
TYPE_CAM_X = 5
TYPE_CAM_Y = 6

motorcommands = [TYPE_MOTOR_1, TYPE_MOTOR_2, TYPE_MOTOR_3]
servocommands = [TYPE_CAM_X, TYPE_CAM_Y]


# Function run on quitting the script
def onquit():
    # Destroy the things which are no longer being used
    cap.release()
    cv2.destroyAllWindows()
    quit()


# Function used by the receiver thread to receive commands for hardware manipulation
def receiving():
    while True:
        rawdata = commsocket.recv(256)
        # Cycle through all the byte-long commands
        for command in rawdata:
            # Extract relevant portions of command
            commandtype = command >> 5
            value = command & 31
            print commandtype
            if commandtype == TYPE_OPTIONS:
                pass
            elif commandtype in motorcommands:
                pass
            elif commandtype == TYPE_LIGHTS:
                pass
            elif commandtype in servocommands:
                pass
            else:
                pass


# Creates and binds to the socket used for communicating with the computer
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 9001))

# Sets the maximum number of connections to 5
serversocket.listen(5)

# Waits and accepts the first one to attempt communication
commsocket, _ = serversocket.accept()
receiver = threading.Thread(target=receiving)
receiver.daemon = True
receiver.start()

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
        commsocket.send(bytearray(frame.flatten()))
        if debug:
            # Display it to the screen, for debugging
            cv2.imshow("frame", frame)
        # Wait, so it works
        cv2.waitKey(1)
