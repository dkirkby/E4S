# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate PWM output driving the internal red LED.
# https://circuitpython.readthedocs.io/en/7.0.x/shared-bindings/pulseio/index.html
#
# For the M4, use board.D13 for the on-board LED.
# For the Pi Pico, use board.GP25 for the on-board LED.
import time
import board
import pwmio

# Use 2 to see individual flashes, 100 for apparent dimming, 20 to see the transition.
FREQUENCY = 2 # Hertz

# Could also drive an external LED from any digital pin (via a series resistor).
PWM = pulseio.PWMOut(board.GP25, frequency=FREQUENCY)

while True:
    for duty_cycle_divisor in (2, 4, 8, 16, 32):
        PWM.duty_cycle = 0xffff // duty_cycle_divisor
        # Could replace sleep with useful work since PWM operates in parallel.
        time.sleep(2)
