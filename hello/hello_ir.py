# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Detect IR light produced by an IR LED.
# Connect the IR LED-photodiode pair so
# the LED is constantly powered and use a
# pull-up to define the pdiode state when
# no IR light is detected:
#
# LED anode & pdiode emitter => GND
# LED cathode => 3.3V with a 1K series resistance
# pdiode collector => D3 with internal pullup
#
# Hold a reflective surface 1-2cm from the IR
# package to bounce enough light into the pdiode
# and change the D3 input level.
import time
import board
import digitalio

D3 = digitalio.DigitalInOut(board.D3)
D3.direction = digitalio.Direction.INPUT
D3.pull = digitalio.Pull.UP

while True:
    print('No IR detected' if D3.value else 'I see the light')
    time.sleep(1)
