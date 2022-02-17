# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Digitize the audio signal captured by either the MEMS or Electret microphone.
#
# There are 3 wires to connect, depending on your microphone + microcontroller:
#
# MEMS Electret |  M4   Pico
# --------------+----------------
#  Vin    Vcc   | 3.3V  3V3(OUT)
#  DC     OUT   | A0    ADC0
#  GND    GND   | GND   GND
# --------------+----------------
#
# The M4 boards can sample the ADC at 28KHz while the Pico achieves 80KHz.
# The electret module is more sensitive than the MEMS module since it includes an
# amplifier.  It also has about double the resolution since it provides a DC offset
# of 50% full scale, instead of about 22% fullscale for the MEMS module.

import time
import math

import board
import analogio

LOG10 = math.log(10)
NSAMPLES = 1024
FULLSCALE = float(0xffff)

mic = analogio.AnalogIn(board.A0)

while True:
    start = time.monotonic_ns()
    samples = [mic.value for i in range(NSAMPLES)]
    stop = time.monotonic_ns()
    # Calculate sampling rate in kHz
    sampling_rate = 1e6 * NSAMPLES / (stop - start)
    # Calculate mean and standard deviation of samples in ADU.
    sum, sumsq = 0, 0
    for i in range(NSAMPLES):
        value = samples[i]
        sum += value
        sumsq += value * value
    mean = sum / NSAMPLES
    stddev = math.sqrt(sumsq / NSAMPLES - mean * mean)
    # Convert to percentages of full scale.
    mean *= 100 / FULLSCALE
    stddev *= 100 / FULLSCALE
    # Calculate a logarithmic "decibel" loudness to display as a horizontal bar.
    # Add eps=1e-8 to avoid log(0).
    loudness = round(25 * max(0, math.log(stddev+1e-8)/LOG10 + 2))
    bar = '#' * loudness
    print(f'rate:{sampling_rate:4.1f}kHz mean:{mean:.1f}% stddev:{stddev:.3f}% {bar}')
    time.sleep(0.1)
