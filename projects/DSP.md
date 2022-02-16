# Project: Digital Signal Processing

In this project you will capture digital samples from the Electret microphone, display a waveform, then perform Fourier spectral analysis to measure the noise floor and identify the dominant frequency present.  We will use the Pico microcontroller since it can sample its ADC at a higher rate than the M4 boards.

You will learn about and apply two digital signal processing techniques: downsampling and fast Fourier transforms (FFT).

## Build the Circuit

Power down your Pico then connect the Electret microphone as follows:
 - Mic Vcc to Pico 3V3(OUT)
 - Mic OUT to Pico A0
 - Mic GND to Pico GND

Start [here](https://en.wikipedia.org/wiki/Electret_microphone) for a brief introduction to electret microphones.  The [adafruit product page](https://www.adafruit.com/product/1063) has more details on the board we are using.

## Read Samples

Use the following program to digitize 512 samples of the microphone signal as fast as possible:
```python
import time

import board
import analogio


NSAMPLES = 512

mic = analogio.AnalogIn(board.A0)

while True:
    time.sleep(1)
    start = time.monotonic_ns()
    samples = [mic.value for i in range(NSAMPLES)]
    stop = time.monotonic_ns()
    duration_ns = stop - start
    print(f'duration = {1e-6*duration_ns:.1f}ms')
```
Each sampling loop should have a duration of about 19ms.  Add code to calculate and print the sampling rate in KHz. Call this sampling rate `f0`.  How does it compare with the upper limit of typical human hearing?

## Plot Samples

Update your code to convert the samples in ADU to millivolts, assuming that the 16-bit full scale corresponds to 3.3V.

Calculate and display the mean signal in mV and compare this with the DC bias printed on the back silkscreen of the microphone module.

Print the first 100 mean-subtracted sample values so that the Mu Editor will display them in its Plotter window.
Note that the Plotter window only displays 100 points at a time, so printing more values to plot would only slow us down without showing more data.

## Audio Test Setup

Use this [online tone generator](https://www.szynalski.com/tone-generator/) to play a continous 440 Hz sine wave through your laptop or phone speaker.  Place the microphone as close as possible to the speaker. With your sample plotting program running, you should see a clear sine wave displayed.  Adjust your setup and volume to get a signal that is 20-30 mV peak to peak.  I recommend some sound insulation between the speaker and your ears since this tone can be annoying.

Note that the Plotter Window automatically scales so the amplitude can appear to suddenly change if the signal falls below 5mV or above 10mV.

## Enhanced Resolution

Since we are able to read samples relatively fast compared with a 440 Hz tone, we can afford to sacrifice some speed for accuracy.  The easiest way to accomplish this is to average consecutive samples, also known as "downsampling".

Modify your code as follows:
```python
NAVG = 8
NMEASURE = 512
NSAMPLES = NAVG * NMEASURE
```
then add code to downsample from `NSAMPLES` samples to `NMEASURE` averages. Call your array of averaged values `measurements`.

Plot the first 100 measurements and compare the new graph with the same audio test setup.  If you did this correctly, the new graph should be compressed along the time axis (by a factor of `NAVG`) and have less noise (by a factor of `sqrt(NAVG)`).  Since `NAVG=2**3` this digital signal processing method has effectively given three extra bits of resolution, at the expense of 8x slower sampling.

## Enter the Frequency Domain

We now want to estimate the frequency of the sine wave in our audio test setup. Our sequence of samples are in the "time domain", where a sine wave has its familar shape.  To identify the frequency of a periodic signal, it is convenient to work instead in the "frequency domain" where a sine wave is delta function at a location determined by its frequency.  Both domains contain exactly the same amount of information and we can move back and forth using [discrete Fourier transforms](https://en.wikipedia.org/wiki/Discrete_Fourier_transform).

To perform a Fourier transform using the standard formulas requires on the order of `NMEASURE**2` floating-point operations.  However, there is a clever way of reorganizing the calculation known as the [fast Fourier transform (FFT)](https://en.wikipedia.org/wiki/Fast_Fourier_transform) which only requires on the order of `NMEASURE * log(NMEASURE)` operations.  The FFT algorithm is implemented in the CircuitPython [ulab library](https://circuitpython.readthedocs.io/en/6.1.x/shared-bindings/ulab/fft/index.html), which implements a subset of the popular [numpy library](https://numpy.org/).  One restriction of the FFT algorithm is that the input array size must be a power of 2, which is why we chose `512 = 2**9` above. (If you ever need the fastest possible FFT algorithm, check out [FFTW](http://www.fftw.org/) which also relaxes the power of two requirement).

Comment out your plotting loop and add code to calculate the Fourier transform of your averaged samples:
```python
measurements = ulab.array(measurements)
fft_real, fft_imag = ulab.fft.fft(measurements)
```
The first line converts your python list of measurement values to the [ulab.array format](https://circuitpython.readthedocs.io/en/6.1.x/shared-bindings/ulab/index.html#ulab.array), which is similar to the [array.array format](https://circuitpython.readthedocs.io/en/6.1.x/docs/library/array.html#array.array.array) we have used earlier.  The second line calculates the FFT and returns two arrays that represent the real and imaginary parts of the complex result.

Why is the FFT result complex valued? This seems to indicate that there is more information in the frequency domain, since we have twice as many array elements, which contradicts what we claimed earlier. However, there is a symmetry that ensures information is conserved,
```python
(fft_real[i] == +fft_real[NMEASURE - i]) and (fft_imag[i] == -fft_imag[NMEASURE - i])
```
for `0 < i < NMEASURE/2`.  Print a few values to convince yourself that this is true (it might not be true
exactly, because of round-off errors, but should be very close).  Because of this symmetry,
all of the information in FFT is contained within the first half of the array `i < NMEASURE/2`. (Technically,
the values with `i > NMEASURE/2` correspond to negative frequencies.)

Although we will not use it in this project, a simple modification of the FFT, known as the "inverse FFT", transforms from the frequency to time domains. Both transforms generally expect a complex-valued input and return a complex-valued result but, when the input is real (or imaginary), the result will have a symmetry that conserves information and ensures that the reverse transform is real (or imaginary).

## Power Play

You can think of the FFT as a recipe for building the time domain signal as a sum of sines and cosines at specific frequencies `f[i] = i * df`, where `df = f0 / (NMEASURE * NAVG)`, with amplitudes related to `fft_real[i]` and `fft_imag[i]` (for `i < NMEASURE/2`). The zero frequency value corresponds to a constant (in time) value, also known as the "DC component".  Since we subtracted off the mean earlier, this should be zero and we will ignore it. (In fact, it will not be exactly zero because of round-off errors in the calculation and subtraction of the mean.)

Since we do not care about the phase differences (sine vs cosine) at each frequency, we will combine the real and imaginary FFT values into their complex magnitude squared, scaled by the number of measurements:
```python
power[i] = (fft_real[i] ** 2 + fft_imag[i] ** 2) / NMEASURE
```
One nice feature of ulab (and numpy) is that you can write a formula that applies to all elements of an array without any explicit loop as:
```python
power = (fft_real ** 2 + fft_imag ** 2) / NMEASURE
```
The resulting `power` is an array, not a single number!  This trick is known as [vectorization](https://blog.paperspace.com/numpy-optimization-vectorization-and-broadcasting/) and leads to code that is cleaner and often faster.

These magnitude squared FFT values are referred to as "power" since they are related to electrical power when the time-domain consists of voltage measurements (but the power terminology is often used for non-voltage measurements).

## Noise Level

Estimate the amount of noise in your measurements with two different methods, one in the time domain and other in the frequency domain:
```python
noise_time = ulab.numerical.std(measurements) ** 2
noise_freq = ulab.numerical.mean(power[1:NMEASURE//2])
```
Calculate and print the results of both of these methods when your setup is relatively quiet. Notice how similar they are!  This is another demonstration that the two domains contain equivalent information, and a consequence of [Parseval's theorem](https://en.wikipedia.org/wiki/Parseval's_theorem).

The first method calculates the [variance](https://en.wikipedia.org/wiki/Variance) of your averaged time-domain samples, i.e. the squared width of a histogram of the samples. The second method calculates the average power over all (positive) frequencies, i.e. excluding the `i=0` DC component and and the `i >= NMEASURE/2` (negative) frequencies that are redundant by symmetry.

Observe typical noise levels when your environment is quiet, then add a line near the top of your program to record the typical level:
```python
NOISE_LEVEL = ...
```

## Frequency Measurement

Now that you have established the typical noise level of your audio environment, you are ready to identify a signal with a dominant frequency that is significantly above the noise level.

Modify your code to loop over the power values for `0 < i < NMEASURE // 2` and find the largest value. If this is at least 1000 times larger than your `NOISE_LEVEL`, then print the corresponding frequency in Hertz, `i * df`.

Test your frequency measurement program with the reference 440 Hz tone.  What is the frequency resolution of your measurement, i.e. what is the smallest difference in frequency that you can detect?  Is your measurement consistent with the known value of 440 Hz given this resolution?  Is this resolution sufficient for a musical instrument tuner?

Test your frequency measurement at different tone frequencies from 220 - 880 Hz (a two octave range).
