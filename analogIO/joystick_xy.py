# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Read and print joystick (x,y) coordinates as analog values.
#
# Make the following connections between the joystick module and microcontroller board:
# Joystick VCC == 3.3V
# Joystick GND == GND
# Joystick Xout == A0
# Joystick Yout == A1
import board
import analogio
import time

Xout = analogio.AnalogIn(board.A0)
Yout = analogio.AnalogIn(board.A1)

while True:
    print((Xout.value, Yout.value)) # print as a tuple for Mu plotter
    time.sleep(0.1) # seconds
