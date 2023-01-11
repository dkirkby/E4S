# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Blink an external LED connected to GP2 of a Pico-W board.
# Use a 1K resistor in series with the LED, either before or after the LED,
# and connect this external circuit to GP2 and GND on the Pico-W board.
# The LED will only work in one orientation so you may need to flip it before it blinks.
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.GP2)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = not led.value # toggle on/off
    time.sleep(0.5) # seconds
