# Audio Input and Output

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

## Introduction

In this activity, you will learn about the two audio components in your [kit](kit.md):
- An [electret microphone with amplifier](https://www.adafruit.com/product/1063)
- A [speaker with audio amplifier](https://www.adafruit.com/product/3885)

Together, these allow you to capture and produce sound.

A nice feature of working with audio is that the frequency range of interest, up to about 20KHz, is slow enough to allow real-time capture and output of audio samples. To verify this, try the following program to capture 4096 ADC samples:
```python
import time
import board
import analogio

NSAMPLES = 4096

ADC = analogio.AnalogIn(board.A0)

while True:

    start = time.monotonic_ns()
    samples = [ADC.value for i in range(NSAMPLES)]
    stop = time.monotonic_ns()

    duration_ns = stop - start
    frequency_Hz = 1e9 / duration_ns * NSAMPLES
    print(f'Sampling duration {1e-6*duration_ns:.1f} ms, frequency {frequency_Hz:.1f} Hz')
    time.sleep(1)
```
This should achieve sampling rates over 80KHz, meaning that we can capture the full audio bandwidth, at least for short durations of about 50 ms.

## Microphone Input

To capture audio data with this program, we only need to attach the microphone to the Pico **ADC0** pin since the microphone module already amplifies and offsets the signal appropriately for ADC input.  The microphone module has three pins to connect:
 - GND connects to the Pico GND
 - VCC connects to the Pico 3.3V
 - OUT connects to any Pico ADC input

Remove USB power, connect your microphone using **ADC0**, then re-run the program above to verify that the sampling rate has not changed.  Next, add some code to calculate the following statistics of the 4096 values captured in the `samples` array:
 - mean value divided by 0xffff
 - standard deviation divided by 0xffff
 - minimum value divided by 0xffff
 - maximum value divided by 0xffff

The full range of the ADC response is 0 - 0xffff, so we divide by 0xffff to map this full range to 0 - 1 for easier interpretation.

Compare the values when the room is quiet (or you cover the microphone) or when you hum or whistle into the microphone. Which values change and which stay the same?

Modify your program to detect sound: it should print either 'QUIET' or 'NOISY' once per second.  Test your program and make changes if needed.

In a [future project](projects/DSP.md) you will dive much deeper into ways of analyzing your captured audio samples.

## Speaker Output

The kit speaker module has three pins to connect, similar to the microphone, but expects an analog output instead of feeding an analog input:
 - Ground connects to the Pico GND
 - 3-5VDC connects to the Pico 3.3V
 - Signal connects to any Pico GP (general-purpose) pin

Note that, since the Pico does not have true analog outputs, we must use a digital (GP) output together with [PWM](aout.md).

Like the microphone module, the speaker module already amplifies and offsets its input signal so that you can provide values in the range 0x0000 - 0xffff.  We will start by outputing a sine wave.  Since trig functions are relatively slow, we precompute the sine wave in a table:
```python
import math
import array

NSAMPLES = 64

sineWaveTable = array.array('H', [0] * NSAMPLES)
for i in range(NSAMPLES):
    sineWaveTable[i] = int((0.5 + 0.5 * math.sin(math.pi * 2 * i / NSAMPLES)) * 0xffff)
    print(f'0x{sineWaveTable[i]:04x} = {sineWaveTable[i] / 0xffff:.4f} * 0xffff')
```
Notice how we use the [array library](https://docs.python.org/3/library/array.html), which is standard python and not CircuitPython specific.  This allows us to use memory more efficiently than native python lists. Also notice how we offset and scale our sine wave to cover the full range of 0x0000 - 0xffff.  Go ahead and run this code and study the printed output.

CircuitPython provides two libraries to help with audio output:
```python
import audiopwmio
import audiocore
```
Using the first library, we can configure any Pico GP pin as a digital output using PWM, for example:
```python
AudioOut = audiopwmio.PWMAudioOut(board.GP22)
```
Using the second library, we can prepare our pre-computed sine wave for audio output:
```python
sineWave = audiocore.RawSample(sineWaveTable)
```
then start looping over this sine wave 220 times per second, leading to a continuous 220 Hz tone (the A below middle C):
```python
sineWave.sample_rate = 220 * NSAMPLES
AudioOut.play(sine_wave, loop=True)
```
Putting all of these pieces together, we can play the tone for 1 second with this code:
```python
import time
import math
import array
import board
import audiocore
import audiopwmio

NSAMPLES = 64

sineWaveTable = array.array('H', [0] * NSAMPLES)
for i in range(NSAMPLES):
    sineWaveTable[i] = int((0.5 + 0.5 * math.sin(math.pi * 2 * i / NSAMPLES)) * 0xffff)
sineWave = audiocore.RawSample(sineWaveTable)

AudioOut = audiopwmio.PWMAudioOut(board.GP22)

def play_tone(frequency, duration):
    sineWave.sample_rate = int(frequency * NSAMPLES)
    if not AudioOut.playing:
        AudioOut.play(waveform, loop=True)
        time.sleep(duration)
    AudioOut.stop()

play_tone(220, 1.0)
```
Try changing the frequency and duration of the note played.  Try repeating the `play_tone` call to play a simple sequence of notes.  How would you introduce a small pause ("rest") between notes?

## A Note Sequencer

In order to simplify playing musical notes, it is helpful to add an extra layer to our software.  First, we can pre-compute the frequencies of each note in a standard musical scale using:
```python
# Define a musical scale starting at 440Hz for A.
note_frequency = {}
for i, note in enumerate('A,A#,B,C,C#,D,D#,E,F,F#,G,G#'.split(',')):
    note_frequency[note] = 440 * math.pow(2, i / 12)
    if note[-1] == '#':
        # Add flat equivalent.
        equiv = 'Ab' if note == 'G#' else chr(ord(note[0]) + 1) + 'b'
        note_frequency[equiv] = note_frequency[note]
```

Next, allow the user to specify a sequence of notes as a string. For example, the string `'1C1,1C1,1D2,1C2,1F2,1E4'` consists of 6 notes, each specified as `<octave><note><beats>` with note being one of `'A,A#,B,C,C#,D,D#,E,F,F#,G,G#'`.
For example, `1C2` plays the note C in the first octave for 2 beats and `2F#1` plays the note F# in the second octave for 1 beat.  Here is a simple note sequencer to accomplish this:
```python
def play_notes(notes, tempo, gap=0.1):
    beat_duration = 60 / tempo
    gap_duration = gap * beat_duration
    for note in notes.split(','):
        octave = int(note[0]) - 1
        beats = int(note[-1])
        duration = (beats - gap) * beat_duration
        play_tone(note_frequency[note[1:-1]] * (1 << octave), duration)
        time.sleep(gap_duration)
```
Notice that this also requires a tempo, specified in beats per minute, and you can optionally specify a small gap (in seconds) between notes.  Add these two functions to your code and test them by ending with:
```python
play_notes('1C1,1C1,1D2,1C2,1F2,1E4', 180)
```
Experiment with changing the tempo and then the notes.
