# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Generate clicks from the speaker and measure them with the Electret microphone.
#
# In order to drive the speaker from a digital line, we need to "bias" (offset)
# the signal by Vcc/2 using a voltage divider consisting of equal resistances R
# connected to Vcc and GND.  We then feed the output from D13 via a capacitance C.
# The resulting circuit has a time constant (R/2)C. Build this biasing circuit
# on the breadboard.
#
# Connect the JST cable to the speaker and wire to the M4 as follows:
# RED => 3.3V
# BLACK => GND
# WHITE => midpoint of voltage divider
#
# Plug the Electret microphone into the breadboard and use jumper wires to connect:
# Vcc => 3.3V
# GND => GND
# OUT => ADC1

import time
import math

import board
import digitalio
import analogio

speaker = digitalio.DigitalInOut(board.D13)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = False

# Initialize an ADC channel to digitize the microphone output.
mic = analogio.AnalogIn(board.A1)

ADU2VOLTS = 3.3 / 0xffff
NSAMPLES = 100

while True:
    speaker.value = True
    speaker.value = True # repeat to stretch out the pulse a bit
    speaker.value = False

    # Record microphone samples as fast as possible.
    start_record = time.monotonic_ns()
    samples = [mic.value for i in range(NSAMPLES)]
    stop_record = time.monotonic_ns()
    duration = 1e-6 * (stop_record - start_record) # ms

    for i in range(NSAMPLES):
        print((samples[i] * ADU2VOLTS,))

    print(f'Sample duration: {duration:.1f}ms')

    time.sleep(1)
