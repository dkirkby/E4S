# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Blink an external LED connected to D12 of a METRO board.
# Use a 1K resistor in series with the LED, either before or after the LED,
# and connect this external circuit to D12 and GND on the METRO board.
# The LED will only work in one orientation so you may need to flip it before it blinks.
#
# Alternatively, change D12 to D13 below which uses the red LED and series resistor
# on the METRO board itself.
#
# For the Pi Pico, use GP25 for the on-board green LED or any GP0-28 for an
# external LED.
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.D12)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = not led.value # toggle on/off
    time.sleep(0.5) # seconds
