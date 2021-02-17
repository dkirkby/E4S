# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Detect 50/60 Hz flicker in the ambient illumination with the AS7341
# connected via the built-in I2C interface.
#
# !!! This program has not yet been demonstrated to work !!!
#
# The following files must be copied to your CIRCUITPY lib/ folder:
#
#  adafruit_as7341.mpy
#  adafruit_bus_device/*
#  adafruit_register/*
#
# Connect the QT-pin cable to the multispec and wire to the M4:
# BLACK => GND
# RED => 3.3V
# BLUE => SDA (serial data)
# YELLOW => SCL (serial clock)
import time

import board

# These files are not in the base CircuitPython installation.
# See instructions above for installing them.
import adafruit_as7341

i2c = board.I2C()

multispec = adafruit_as7341.AS7341(i2c)

# Configure the LED.
multispec.led_current = 0 # mA
multispec.led = False

# Enable flicker detection.
multispec.flicker_detection_enabled = True

last = 0
while True:
    flicker = multispec.flicker_detected
    if flicker != last:
        if flicker is None:
            print('No flicker detected.')
        else:
            print(f'Detected flicker at {flicker} Hz.')
        last = flicker
    time.sleep(0.1)
