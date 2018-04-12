# This code is in PYTHON2 and runs on the RPi

import cv2
import RPi.GPIO as r
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

# The header numbers that correspond to the pin numbers by index
pins = [11, 12, 13, 15, 16, 18,
        22,  7,  3,  5, 24, 26,
        19, 21, 23,  8, 10]

# Give names to the first 9 pins
motorpowpins = pins[:3]
motordirpins = pins[3:6]
lightingpin = pins[6]
servopins = pins[7:9]

# Set up the output pins
print "Initialise GPIO"
r.setwarnings(False)
r.setmode(r.BOARD)
r.setup(pins[:9], r.OUT)
r.output(pins[:9], False)

# Set up the servo PWM
servopwm = [r.PWM(i, 50) for i in servopins]


# Function run on quitting the script
def onquit():
    # Destroy the things which are no longer being used
    cap.release()
    cv2.destroyAllWindows()
    r.cleanup()
    quit()


# Function used by the receiver thread to receive commands for hardware manipulation
def receiving():
    while True:
        rawdata = commsocket.recv(256)
        # Cycle through all the byte-long commands
        for command in rawdata:
            command = ord(command)
            # Extract relevant portions of command
            commandtype = command >> 5
            value = command & 31
            if commandtype == TYPE_OPTIONS:
                pass
            elif commandtype in motorcommands:
                pass
            elif commandtype == TYPE_LIGHTS:
                # Probably output serial to a shift register (i.e. 4021 chip), controlling an array of LEDs
                pass
            elif commandtype in servocommands:
                servono = servocommands.index(commandtype)
                # If the most significant bit is high, it should be -ve
                if value >> 4:
                    # Set all bits above the most significant bit high, signifying -ve
                    value |= -32
                servoangle = value * 3
                dutycycle = (45 + servoangle) * (100.0/90.0)
                print "Servo {}'s angle set to {} (Duty Cycle = {})".format(servono,
                                                                            servoangle,
                                                                            dutycycle)
                servopwm[servono].start(dutycycle)
            else:
                pass


# Create and bind to the socket used for communicating with the computer
print "Start server"
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 9001))

# Set the maximum number of connections to 5
serversocket.listen(5)

# Wait and accept the first one to attempt communication
print "Awaiting connection..."
commsocket, _ = serversocket.accept()
print "Connected to {}".format(commsocket.getpeername())
receiver = threading.Thread(target=receiving)
receiver.daemon = True
receiver.start()

# Open Webcam
print "Connect to camera"
cap = cv2.VideoCapture(0)  # 0 signifies the first available camera device

# The protocol used for video
fourcc = cv2.cv.FOURCC(*"XVID")

print "Display and send video feed"
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
