# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Read out the ultrasonic distance sensor.
# Make the following connections between the sensor and Pico.
# VCC = 3.3V
# GND = GND
# TRIG = GP21
# ECHO = GP22
import time
import board
import adafruit_hcsr04

# See https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP21, echo_pin=board.GP22)

NAVG = 16

while True:
    distance = 0.
    nsamples = 0
    for i in range(NAVG):
        # The measurement will sometimes time out, resulting in a RuntimeError.
        # Therefore we cannot assume we will get NAVG samples and must count them.
        try:
            distance += sonar.distance
            nsamples += 1
        except RuntimeError:
            pass
    distance /= nsamples
    print((distance,))
    time.sleep(0.1)
