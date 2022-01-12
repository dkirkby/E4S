# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Read and display joystick (x,y) coordinates as analog values.
#
# Make the following connections between the joystick module and microcontroller board
# (either of the M4s or the Pico):
#
# Joystick    M4     Pico
# ---------  -----  ------
#   GND       GND  = GND
#   VCC       3.3V = 3.3V(OUT)
#   Xout      A0   = ADC0
#   Yout      A1   = ADC1
#
# Pi Pico pinouts are list here:
# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/pinouts
#
# Open the Plotter tab in the Mu editor to see a plot of the numbers printed.

import board
import analogio
import time

Xout = analogio.AnalogIn(board.A0)
Yout = analogio.AnalogIn(board.A1)

while True:
    print((Xout.value, Yout.value)) # print as a tuple for Mu plotter
    time.sleep(0.1) # seconds
