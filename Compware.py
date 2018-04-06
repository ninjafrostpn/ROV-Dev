# This code is in PYTHON3 and runs on the surface-side interface

import threading
import socket
import os
import numpy as np
import cv2
import pygame
from pygame.locals import *
from time import time

debug = True
starttime = time()

# Options for command 3-bit command code
TYPE_OPTIONS = 0
TYPE_MOTOR_1 = 1
TYPE_MOTOR_2 = 2
TYPE_MOTOR_3 = 3
TYPE_LIGHTS = 4
TYPE_CAM_X = 5
TYPE_CAM_Y = 6


roundconstrain = lambda val, lo, hi: round(min(max(val, lo), hi))


# Debug-log printer
def qrint(*args, **kwargs):
    print("-- {:} ({:.03f}s) --".format(time(), time() - starttime))
    print(*args, **kwargs)


# Function run on quitting the script
def onquit():
    qrint("Shutting down...")
    # Allow things to be gotten rid of, as necessary
    if recording:
        out.release()
    if debug:
        cap.release()
    quit()


# Function for outputting seconds as hoursminutesseconds
def HMS(val):
    ss_ss = val % 60
    mm = (val - ss_ss) % 3600
    hh = (val - (mm + ss_ss))
    return "{:n}h{:n}m{:.2f}s".format(hh / 3600, mm / 60, ss_ss)


# Function used by the receiver thread to receive image data sent by the Pi
def receiving():
    rawdata = bytes()
    if debug:
        qrint("Starting camera")
        while True:
            ret, frame[:] = cap.read()
            if ret:
                # qrint(frame.dtype, frame.shape)
                cv2.imshow("frame", frame)
                cv2.waitKey(1)
    else:
        while True:
            # Receive as many bytes as required to get a whole image
            rawdata += commsocket.recv(921600) # (921600 = 640px wide x 480px tall x 3 colours (R, G, and B))
            # If enough has been collected to possibly represent a whole image
            if len(rawdata) >= 921600:
                # Remove one image's worth of data from the beginning of that received
                rawdata, framedata = rawdata[921600:], rawdata[:921600]
                # Update the on-screen video feed with the data received
                # (After translating it into an image from the bytes)
                frame[:] = np.frombuffer(framedata, dtype=np.uint8).reshape(480, 640, 3)


class CommandError(Exception):
    pass


# Function used to send commands for hardware manipulation by the Pi
def sendcommand(commandtype, value):
    if commandtype < 0 or commandtype > 7:
        raise CommandError
    # First three bits of a byte identify the item being commanded
    # Last five bits of a byte give the value assigned to it
    # E.g. 10011111 = Lights (100) Turn them all on (11111)
    #      00100111 = Motor 1 (001) Set to about half speed forward (00111)
    #      01001111 = Motor 2 (010) Set to full speed reverse (11111)
    command = commandtype << 5  # Puts identification bits to front
    command |= 31 & value       # Inserts value to be sent
    commsocket.send(command)    # And sends it


# Initialise output variables
motors = [0, 0, 0]
motorcommand = [TYPE_MOTOR_1, TYPE_MOTOR_2, TYPE_MOTOR_3]
lights = [False, False, False, False, False]
servos = [0, 0]


# Function used to change motor speeds
def setmotor(which, speed):
    speed = roundconstrain(speed, -15, 15)
    if motors[which] != speed:
        motors[which] = speed
        sendcommand(motorcommand[which], speed)


# Function used to switch lights on and off
def setlight(which, state):
    # State is boolean representing "Light is on" (any value below or at 0 counts as False, else True)
    state = state > 0
    if lights[which] != state:
        lights[which] = state
        lightvalue = 0
        for light in lights:
            lightvalue <<= 1
            lightvalue |= light
        sendcommand(TYPE_LIGHTS, lightvalue)


# Function used to set the rotation of the camera positioning servos
def setcameraangle(x, y):
    # x and y are input as values between -45 and 45 degrees, with a resolution of 3 degrees
    x = roundconstrain(x/3, -15, 15)
    y = roundconstrain(y/3, -15, 15)
    if servos[0] != x:
        servos[0] = x
        sendcommand(TYPE_CAM_X, x)
    if servos[1] != y:
        servos[1] = y
        sendcommand(TYPE_CAM_Y, y)


# Initialise the video feed as a blank, black screen
frame = np.zeros((480, 640, 3), dtype=np.uint8)

# The protocol used for video
fourcc = cv2.VideoWriter_fourcc(*"XVID")

if not debug:
    # The IP and socket number used for comms with teh Pi
    piaddr = ("169.254.198.75", 9001)
    piaddr2 = ("192.168.1.97", 9001)
    
    # The socket used for comms with teh Pi
    connected = False
    qrint("Connecting...")
    commsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while not connected:
        try:
            commsocket.connect(piaddr)
            connected = True
        except ConnectionRefusedError:
            pass
    qrint("Connected to {}".format(commsocket.getpeername()))
else:
    qrint("##DEBUG MODE##")
    cap = cv2.VideoCapture(0)  # 0 signifies the first available camera device

# Start the receiver thread
# This is daemonic, so that it finishes when the main thread does and doesn't stop the program closing
receiver = threading.Thread(target=receiving, daemon=True)
receiver.start()

# Creates a folder for saved videos and images to go into in the current working directory
path = os.getcwd() + r"\ROV-Captures"
try:
    os.mkdir(path)
    qrint("Created ROV-captures folder")
except FileExistsError:
    qrint("ROV-Captures folder already exists")
path += r"\DIVE{:.0f}".format(time())
os.mkdir(path)
qrint("Created folder for this session. Captures will be saved to:\n" + path)

# Define some colours
white = (255, 255, 255)
black = 0
red = (255, 0, 0)
green = (0, 255, 0)
blue = (50, 0, 255)

# Set up the pygame window
pygame.init()
pygame.display.set_caption("Camera-Vision")
screen = pygame.display.set_mode((1000, 480))
w = screen.get_width()
h = screen.get_height()

# Load up a nice font
smallfont = pygame.font.Font(None, 30)

# Initialise variables which indicate state
recording = False  # "The camera is recording video"
camon = True  # "The camera is to stay on for the next cycle"

# Initialise capture variables
recordname = "VIDEO"
recordstarttime = -1
recordfinishtime = -1
recordcount = 0
totalrecordtime = 0
photoname = "PHOTO"
phototime = -1
photocount = 0

# Main draw loop
qrint("Display video feed")
while True:
    # Converts from opencv image capture to pygame Surface
    pframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pframe = np.rot90(np.fliplr(pframe))
    # qrint(pframe.shape)
    pframe = pygame.surfarray.make_surface(pframe)
    # qrint(pframe.get_size())
    
    # Draw everything
    screen.fill(black)
    screen.blit(pframe, (0, 0))
    pygame.draw.line(screen, white, (640, 0), (640, h))
    if recording:
        # Record frames if recording
        out.write(frame)
        # Show red recording circle
        pygame.draw.circle(screen, red, (15, 15), 10)
        # Update the potential end time of the recording
        recordfinishtime = time()
    # If a photo has just been taken (0.1s ago or less)
    if time() - phototime < 0.1 and photocount > 0:
        # Shows a blue circle
        pygame.draw.circle(screen, blue, (40, 15), 10)
    # Generates the readout on the right
    messages = [["Activity this session:", green],
                ["  Time: {}".format(HMS(time() - starttime)), green],
                ["Recordings:", red],
                ["  Time: {}".format(HMS(recordfinishtime - recordstarttime) if recordcount > 0 else "None"), red],
                ["  Total: {}".format(HMS(totalrecordtime)), red],
                ["  Count: {} videos".format(recordcount), red],
                ["Photos:", blue],
                ["  Count: {} photos".format(photocount), blue],
                ["  Recent: {}".format(HMS(time() - phototime) if photocount > 0 else "None"), blue]]
    # Actually draws the readout
    for i, m in enumerate(messages):
        screen.blit(smallfont.render(m[0], True, m[1]), (650, 40 * i))
    # Draw everything to the display
    pygame.display.flip()
    
    # Event handling
    for e in pygame.event.get():
        # If window's x is pressed, prepare to leave
        if e.type == QUIT:
            onquit()
        elif e.type == KEYDOWN:
            # If enter is pressed, take a photo
            if e.key == K_RETURN:
                photocount += 1  # So that photo indexing starts at 00001
                photoname = path + r"\IMG{:05d}.png".format(photocount)
                qrint("Took photo #{}, saved to:\n{}".format(photocount, photoname))
                cv2.imwrite(photoname, frame)
                phototime = time()
            # If r is pressed, start or stop recording
            if e.key == K_r:
                if not recording:
                    recordcount += 1  # So that video indexing starts at 00001
                    recordname = path + r"\VID{:05d}.avi".format(recordcount)
                    out = cv2.VideoWriter(recordname, fourcc, 20, (640, 480))
                    recordstarttime = time()
                    qrint("Recording #{} to:\n{}".format(recordcount, recordname))
                else:
                    qrint("Recording #{} ended, saved to:\n{}".format(recordcount, recordname))
                    out.release()
                    totalrecordtime += recordfinishtime - recordstarttime
                recording = not recording
            # If escape is pressed... as with the red x
            if e.key == K_ESCAPE:
                onquit()
