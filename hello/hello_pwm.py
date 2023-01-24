# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate pulse-width modulation (PWM) output driving an LED.
#
# See https://dkirkby.github.io/E4S/aout.html for more information.
#
# Use jumper wires to build the following circuit:
# GP22 => 1K resistor => LED => GND
import time
import board
import pwmio

# Specify the PWM cycle frequency in Hertz.
# Use 8 to see individual flashes, 100 for apparent dimming, 20 to see the transition.
# The minimum Pico W frequency is 8 Hertz.
FREQUENCY = 8

# Initialize a PWM output. For details, see
# https://docs.circuitpython.org/en/latest/shared-bindings/pwmio/index.html
PWM = pwmio.PWMOut(board.GP22, frequency=FREQUENCY)

while True:
    for value in (0xffff, 0xc000, 0x8000, 0x4000):
        print(f'duty_cycle = 0x{value:04x} / 0xffff = {100*value/0xffff:.1f}%')
        PWM.duty_cycle = value
        # Could replace sleep with useful work since PWM operates in parallel.
        time.sleep(2)
