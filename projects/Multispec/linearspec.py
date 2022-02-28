# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Read light levels from the AS7341
# connected via the built-in I2C interface.
# Convert measured fluxes in each band to linearly interpolated fluxes
# that are corrected for the spectral response of each filter.
#
# See hello_multispec.py for an example of how to read fluxes
# in each band using the AS7341.
#
# The following files must be copied to your CIRCUITPY lib/ folder:
#
#  adafruit_as7341.mpy
#  adafruit_bus_device/*
#  adafruit_register/*
#
# See https://github.com/adafruit/Adafruit_CircuitPython_AS7341
# for details on the AS7341 library and examples.
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

import ulab.numpy as np

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

# Use a low gain to avoid saturating in full sunlight.
multispec.gain = adafruit_as7341.Gain.GAIN_2X

# List the available bands.
bands = ['415nm','445nm','480nm','515nm','555nm','590nm','630nm','680nm','clear','nir']
nbands = len(bands)

# Configure the on-board white LED.
multispec.led = False
multispec.led_current = 25 # mA

# Disable flicker detection.
multispec.flicker_detection_enabled = False

# Matrix to transform measured band fluxes to linearly interpolation fluxes.
inverse = np.ndarray([
	[0.22405, 0.0070204, -0.00019178, 7.0214e-06, -5.5096e-07, 6.1549e-08, -5.3523e-09, 5.3565e-10],
	[-0.10948, 0.17198, -0.0046982, 0.00017201, -1.3497e-05, 1.5078e-06, -1.3112e-07, 1.3122e-08],
	[0.082699, -0.13312, 0.13831, -0.0050636, 0.00039733, -4.4386e-05, 3.8599e-06, -3.8629e-07],
	[-0.058369, 0.094059, -0.10195, 0.10065, -0.007898, 0.0008823, -7.6726e-05, 7.6785e-06],
	[0.036403, -0.058665, 0.06372, -0.065853, 0.08282, -0.0094219, 0.00081938, -8.2002e-05],
	[-0.025095, 0.040442, -0.043931, 0.04551, -0.059966, 0.07946, -0.0069283, 0.00069337],
	[0.01624, -0.026172, 0.02843, -0.02946, 0.039023, -0.058678, 0.056136, -0.0056246],
	[0.0012445, -0.0020056, 0.0021787, -0.0022575, 0.0029879, -0.0044096, 0.003658, 0.016792],
])

nband = 8
band_flux = np.zeros(nband)
linear_flux = np.zeros(nband)
linear_wlen = np.linspace(420, 680, 8)

nplot = 100
plot_wlen = np.linspace(linear_wlen[0], linear_wlen[-1], nplot)
plot_flux = np.zeros(nplot)

navg = 8
while True:
    # Calculate means of navg readings in each band.
    band_flux[:] = 0
    for i in range(navg):
        for j, band in enumerate(bands[:nband]):
            band_flux[j] += getattr(multispec, 'channel_' + band)
    band_flux /= navg
    ##print('  band:', ','.join([f'{band_flux[i]:.3f}' for i in range(nband)]))
    # Convert measured band fluxes to linearly interpolated fluxes.
    linear_flux[:] = np.dot(inverse, band_flux)
    ##print('linear:', ','.join([f'{linear_flux[i]:.3f}' for i in range(nband)]))
    # Interpolate linear model for plotting.
    plot_flux[:] = np.interp(plot_wlen, linear_wlen, linear_flux)
    # Print the data to plot in the Mu Editor.
    for j in range(nplot):
        print((plot_flux[j],))
