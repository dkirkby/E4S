# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Control the AC relay using a single digital output.
# Pull out the green terminal block and use a small
# slotted screwdriver to fasten two long jumper wires.
# Connect the "-" jumper wire to the M4 GND.
# Connect the "+" jumper wire to the M4 D2.
import time
import board
import digitalio

D2 = digitalio.DigitalInOut(board.D2)
D2.direction = digitalio.Direction.OUTPUT
D2.value = False

while True:
    # You should hear a loud click each second from the relay box,
    # and the green LED on the relay box will be on when D2 is True.
    print(D2.value)
    time.sleep(1)
    D2.value = not D2.value
