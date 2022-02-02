# Raspberry Pi Pico

The Pico is a small, low cost ($4) microcontroller board designed by the Raspberry Pi foundation based on a powerful and low-cost new chip, the RP2040.

Useful links:
 - Pico Board
   - [Getting started with the Pico](https://projects.raspberrypi.org/en/projects/getting-started-with-the-pico/0)
   - [Datasheet](https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf)
 - CircuitPython for the Pico
   - [Getting started](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython)
   - [Downloads](https://circuitpython.org/board/raspberry_pi_pico/)
 - RP2040
   - [Official documentation](https://www.raspberrypi.com/documentation/microcontrollers/rp2040.html)
   - [Datasheet](https://datasheets.raspberrypi.com/rp2040/rp2040-datasheet.pdf) (654 pages!)

Since the silkscreen labels for each pin are on the bottom side of the board, the following diagram is very helpful (more sizes are available [here](https://learn.adafruit.com/assets/99339)):

![Pico Pinout](https://raw.githubusercontent.com/dkirkby/E4S/master/img/pico-pinout.png)

## Differences with the Metro M4

A Metro M4 Express board can often be replaced with the smaller and cheaper Pico, with the following changes:
 - The internal LED is GP25 instead of D13 (and red instead of green).
 - Digital pins are designated GP0 - GP28, instead of D0 - D13.
 - Analog pins are A0 - A3 but there is no A4 or A5.

For any board supported by CircuitPython, you can list its predefined pins using:
```python
import board
print(dir(board))
```

The Pico is not a direct substitute when:
 - You need the M4 on-board NEO pixel.
 - You need to power your board from the 9V DC transformer.
 - You need the full CPU power or memory size of the faster M4 processor.

The Pico includes advanced programmable input/output (PIO) hardware that allows any of the general-purpose (GP) pins to used for hardware-level PWM or communications protocols.  For example, to use `GP14` for PWM at 1kHz, use:
```python
import board
import pwmio

pwm = pwmio.PWMOut(board.GP14, frequency=1000)
```
Similarly, to use `GP0` and `GP1` to run an I2C bus, use:
```python
import board
import busio

i2c = busio.I2C(sda=board.GP0, scl=board.GP1)
```
