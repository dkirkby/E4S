# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Read the pressure and temperature from the DPS310
# connected via the built-in I2C interface.
#
# The following files must be copied to your CIRCUITPY lib/ folder:
#
#  adafruit_dps310.mpy
#  adafruit_bus_device/*
#  adafruit_register/*
#
# Connect the QT-pin cable to the pressure sensor and wire to the M4:
# BLACK => GND
# RED => 3.3V
# BLUE => SDA (serial data)
# YELLOW => SCL (serial clock)
import time

import board

# This file is not in the base CircuitPython installation.
# See instructions above for installing it and its dependencies.
import adafruit_dps310

i2c = board.I2C()

tpsensor = adafruit_dps310.DPS310(i2c)

while True:
    temperature = tpsensor.temperature
    pressure = tpsensor.pressure
    print(f'T = {temperature:.2f} C, P = {pressure:.2f} hPa')
    time.sleep(1)
