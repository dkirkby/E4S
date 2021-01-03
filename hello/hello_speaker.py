# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Play sine-wave tones from the STEMMA speaker.
import time
import math

import board
import audiocore
import audioio
import array

# Fill a buffer with a 16-bit unsigned integer sine waveform.
NSINE = 64
buffer = array.array("H", [0] * NSINE)
omega = 2 * math.pi / NSINE
for i in range(NSINE):
    x = math.sin(i * omega)
    k = int(x * 0x7fff) + 0x8000
    #print(f'{i:2d} : {x:.3f} -> {k:04x}')
    buffer[i] = k
waveform = audiocore.RawSample(buffer)

# Play a tone of the specified frequency (Hz) and duration (sec).
def play_tone(freq, duration, DAC):
    waveform.sample_rate = int(freq * NSINE)
    if not DAC.playing:
        DAC.play(waveform, loop=True)
        time.sleep(duration)
    DAC.stop()

# Define a musical scale starting at 440Hz for A.
note_frequency = {}
for i, note in enumerate('A,A#,B,C,C#,D,D#,E,F,F#,G,G#'.split(',')):
    note_frequency[note] = 440 * math.pow(2, i / 12)
    if note[-1] == '#':
        # Add flat equivalent.
        equiv = 'Ab' if note == 'G#' else chr(ord(note[0]) + 1) + 'b'
        note_frequency[equiv] = note_frequency[note]

# Play musical notes at a specified tempo in beats per minute.
# Each note has the format <octave><note><beats>, e.g. 1C2 plays
# C in the first octave for 2 beats and 2F#1 plays F# in the second
# octave for 1 beat.  Gap is the space between notes in beats.
def play_notes(notes, tempo, DAC, gap=0.1):
    beat_duration = 60 / tempo
    gap_duration = gap * beat_duration
    for note in notes.split(','):
        octave = int(note[0]) - 1
        beats = int(note[-1])
        duration = (beats - gap) * beat_duration
        play_tone(note_frequency[note[1:-1]] * (1 << octave), duration, DAC)
        time.sleep(gap_duration)
