# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate the on-board neopixel RGB LED.
# https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels
# Wavelengths are R~625nm, G~522nm, B~470nm.
# No wiring is required.
import time
import board
import neopixel

led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.01

while True:
    # One LED on at a time
    led[0] = (0, 0, 0)
    time.sleep(0.5)
    led[0] = (255, 0, 0)
    time.sleep(1)
    led[0] = (0, 0, 0)
    time.sleep(0.5)
    led[0] = (0, 255, 0)
    time.sleep(1)
    led[0] = (0, 0, 0)
    time.sleep(0.5)
    led[0] = (0, 0, 255)
    time.sleep(1)
    # One LED off at a time.
    led[0] = (255, 255, 255)
    time.sleep(0.5)
    led[0] = (0, 255, 255)
    time.sleep(1)
    led[0] = (255, 255, 255)
    time.sleep(0.5)
    led[0] = (255, 0, 255)
    time.sleep(1)
    led[0] = (255, 255, 255)
    time.sleep(0.5)
    led[0] = (255, 255, 0)
    time.sleep(1)
