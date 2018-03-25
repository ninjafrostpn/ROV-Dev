# This code is in PYTHON3 and runs on the surface-side interface

import threading
import socket
import os
import numpy as np
import cv2
import pygame
from pygame.locals import *
from time import time

# The IP and socket number used for comms with teh Pi
piaddr = ("169.254.198.75", 9001)

# The socket used for comms with teh Pi
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(piaddr)

# Initialise the video feed as a blank, black screen
frame = np.zeros((480, 640, 3), dtype=np.uint8)

# The protocol used for video
fourcc = cv2.VideoWriter_fourcc(*"XVID")

# Function used by the receiver thread to receive image data sent by the Pi
def receiving():
    rawdata = bytes()
    while True:
        # Receive as many bytes as required to get a whole image
        rawdata += s.recv(921600) # (921600 = 640px wide x 480px tall x 3 colours (R, G, and B)
        # If enough has been collected to possibly represent a whole image
        if len(rawdata) >= 921600:
            # Remove one image's worth of data from the beginning of that received
            rawdata, framedata = rawdata[921600:], rawdata[:921600]
            # Update the on-screen video feed with the data received
            # (After translating it into an image from the bytes)
            frame[:] = np.frombuffer(framedata, dtype=np.uint8).reshape(480, 640, 3)

# Start the receiver thread
receiver = threading.Thread(target=receiving)
receiver.start()

# Creates a folder for saved videos and images to go into in the current working directory
path = os.getcwd() + r"\ROV-Captures"
try:
    os.mkdir(path)
except FileExistsError:
    pass
os.mkdir(path + "\{:.0f}".format(time()))

# Define some colours
white = (255, 255, 255)
black = 0
red = (255, 0, 0)
green = (0, 255, 0)
blue = (50, 0, 255)


# Function for outputting seconds as hoursminutesseconds
def HMS(val):
    s = val % 60
    m = (val - s) % 3600
    h = (val - (m + s))
    return "{:n}h{:n}m{:.2f}s".format(h / 3600, m / 60, s)


# Set up the pygame window
pygame.init()
pygame.display.set_caption("Camera-Vision")
screen = pygame.display.set_mode((1000, 480))
w = screen.get_width()
h = screen.get_height()

# Load up a nice font
smallfont = pygame.font.Font(r"D:\Users\Charles Turvey\Documents\Python\Projects\OpenSans-Regular.ttf", 30)

# Initialise variables which indicate state
recording = False  # "The camera is recording video"
camon = True  # "The camera is to stay on for the next cycle"

# Initialise stats
starttime = time()
recordstarttime = -1
recordfinishtime = -1
recordcount = 0
totalrecordtime = 0
phototime = -1
photocount = 0

# Main draw loop
while camon:
    # Converts from opencv image capture to pygame Surface
    pframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pframe = np.rot90(np.fliplr(pframe))
    # print(pframe.shape)
    pframe = pygame.surfarray.make_surface(pframe)
    # print(pframe.get_size())
    
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
            camon = False
        elif e.type == KEYDOWN:
            # If enter is pressed, take a photo
            if e.key == K_RETURN:
                photocount += 1
                cv2.imwrite("IMG{}/{:.0f}.png".format(path, time()), frame)
                phototime = time()
            # If r is pressed, start or stop recording
            if e.key == K_r:
                if not recording:
                    recordcount += 1
                    out = cv2.VideoWriter("VID{}/{:.0f}.avi".format(path, time()), fourcc, 20, (640, 480))
                    recordstarttime = time()
                else:
                    out.release()
                    totalrecordtime += recordfinishtime - recordstarttime
                recording = not recording
            # If escape is pressed... as with the red x
            if e.key == K_ESCAPE:
                camon = False

# Allow things to be gotten rid of, as necessary
if recording:
    out.release()
