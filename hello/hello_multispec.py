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
# Connect the QT-pin cable to the display and wire to the M4:
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

wavelengths = [415, 445, 480, 515, 555, 590, 630, 680]
names = [f'channel_{w}nm' for w in wavelengths]

LINE_LENGTH = 80

separator = '-' * LINE_LENGTH

def bar(value, max_value=10000, max_length=LINE_LENGTH - 6):
    length = int(round((value / max_value) * max_length))
    return '#' * length

while True:
    fluxes = [getattr(multispec, name) for name in names]
    for (wavelength, flux) in zip(wavelengths, fluxes):
        print(f'{wavelength}nm {bar(flux)}')
    print(separator)
    time.sleep(1)
