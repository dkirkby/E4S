# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Read light levels from the AS7341
# connected via the built-in I2C interface.
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
import math

import board
import busio

try:
    # SDA, SCL are predefined on M4
    sda, scl = board.SDA, board.SCL
except:
    # Use SDA=GP0, SCL=GP1 on Pico
    sda, scl = board.GP0, board.GP1

i2c = busio.I2C(sda=sda, scl=scl)

# These files are not in the base CircuitPython installation.
# See instructions above for installing them.
import adafruit_as7341

multispec = adafruit_as7341.AS7341(i2c)

# The clear and NIR sensor readings are not yet supported.
wavelengths = [415, 445, 480, 515, 555, 590, 630, 680]

# On board "white" LED provides consistent illumination for measuring
# the spectrum of reflected light from a surface.
USE_LED = True

# Configure the LED.
multispec.led_current = 25 # mA
multispec.led = USE_LED

# Disable flicker detection.
multispec.flicker_detection_enabled = False

# Display a simple horizontal histogram using text.
LINE_LENGTH = 120

separator = '-' * LINE_LENGTH

def bar(value, max_value=10000, max_length=LINE_LENGTH - 11):
    length = int(round((value / max_value) * max_length))
    return '#' * length

# Main loop reads sensors and displays the measured spectrum.
LOG2 = math.log(2)
while True:
    fluxes = multispec.all_channels
    log2_fluxes = [math.log(max(1,flux)) / LOG2 for flux in fluxes]
    for i, wavelength in enumerate(wavelengths):
        print(f'{wavelength}nm {fluxes[i]:04x} {bar(log2_fluxes[i], max_value=16)}')
    print(separator)
    time.sleep(0.5)
