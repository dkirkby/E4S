# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Read and display joystick inputs.
# Connect jumper cables to the joystick and wire to M4:
# Vcc => 3.3V
# Xout => A0
# Yout => A1
# Sel => D2
# GND => GND
import time

import board
import analogio
import digitalio

Xout = analogio.AnalogIn(board.A0)
Yout = analogio.AnalogIn(board.A1)

SEL = digitalio.DigitalInOut(board.D2)
SEL.direction = digitalio.Direction.INPUT
SEL.pull = digitalio.Pull.UP

while True:
    print((Xout.value, Yout.value, SEL.value * 0xffff))
    time.sleep(0.1)
