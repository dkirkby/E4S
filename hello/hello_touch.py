# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S

# Connect a jumper wires from GP4 and 3.3V to the breadboard.
# Put a 10MOhm resistor across GP4 and 3.3V on the breadboard.
# Connect an unterminated wire to GP4 from the breadboard.
# Touch the end of the unterminated wire to see the touch sensor in action.

# See https://docs.circuitpython.org/en/latest/shared-bindings/touchio/ for details

import time
import board
import touchio
import digitalio

touch = touchio.TouchIn(board.GP4, pull=digitalio.Pull.UP)

while True:
    print('YES' if touch.value else 'no')
    time.sleep(0.2)
