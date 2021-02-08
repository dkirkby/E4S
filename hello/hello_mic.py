# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Digitize the audio signal captured by the MEMS microphone.
#
# Connect:
# Mic Vin - M4 3.3V
# Mic GND - M4 GND
# Mic DC - M4 A0
import time

import board
import analogio
import array

BUFFER_SIZE = 1024
BUFFER_DURATION = 0.1

mic = analogio.AnalogIn(board.A0)

buffer = array.array("H", [0] * BUFFER_SIZE)

fullscale = float(0xffff)

while True:
    print('Sampling...')
    nsamples = 0
    start = time.monotonic()
    stop_by = start + BUFFER_DURATION
    while (time.monotonic() < stop_by) and (nsamples < BUFFER_SIZE):
        buffer[nsamples] = mic.value
        nsamples += 1
    # Calculate the actual sampling parameters.
    duration = time.monotonic() - start
    sampling_rate = nsamples / duration
    print(f'Captured {nsamples} samples over {duration:.4f}s at {sampling_rate:.1f}Hz.')
    # Calculate sampled signal statistics.
    sum = 0
    sumsq = 0
    for i in range(nsamples):
        value = buffer[i]
        sum += value
        sumsq += value * value
    mean = sum / nsamples
    stddev = sumsq / nsamples - mean * mean

    print(f'Sample mean = {mean:.1f} ADU ({1e2*mean/fullscale:.1f}%), std dev = {stddev:.1f} ADU ({stddev/fullscale:.1f}%)')

    time.sleep(0.5)
