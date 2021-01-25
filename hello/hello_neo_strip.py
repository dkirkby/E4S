# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate the 8-neopixel RGB LED strip.
# https://learn.adafruit.com/adafruit-neopixel-uberguide/the-magic-of-neopixels
# Wavelengths are R~625nm, G~522nm, B~470nm.

# Each RGB units draws ~60mA with all LEDs on a max brightness,
# so turning all 8 units on draws 0.48A, very close to the maximum
# of 0.5A available from USB-1,2 and enforced with a fuse.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Turn off power before connecting the strip as follows:
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# M4 GND - GND strip (only need to connect one of these)
# M4 D2 - DIN strip
# M4 3.3V - 5VDC strip (less than 5V is ok)
import time
import board
import neopixel

NLEDS = 8
leds = neopixel.NeoPixel(board.D2, NLEDS, auto_write=False)
leds.brightness = 0.01

OFF = (0, 0, 0)
ON = (255, 0, 0)

while True:
    # Cycle through LEDs to turn on, one at a time.
    for i in range(NLEDS):
        for j in range(NLEDS):
            leds[j] = ON if i == j else OFF
        leds.show()
        time.sleep(1)
