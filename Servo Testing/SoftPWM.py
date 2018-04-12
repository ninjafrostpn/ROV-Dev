# PYTHON2 file to be run on the Pi Zero
import RPi.GPIO as r
from time import sleep
from math import cos, radians

r.setmode(r.BOARD)

pins = [11, 12, 13, 15, 16, 18,
        22,  7,  3,  5, 24, 26,
        19, 21, 23,  8, 10]

r.setup(pins[0], r.OUT)

pwm = r.PWM(pins[0], 50)

i = 0
while True:
    pwm.start(50 * (1 - cos(radians(i))))
    i += 1
    sleep(0.01)
