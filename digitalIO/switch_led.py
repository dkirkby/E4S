# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Control an external LED connected to D12 of a METRO board using an
# external switch connected to D2, with an optional internal pullup.
# You can use the Sel and GND pins of the kit joystick for the switch.
#
# Without an internal pullup, the switch will cause an open-circuit
# condition when it is open.  You can either fix this by added an
# external pullup resistor (e.g. 10Kohm), or enable the internal pullup
# resistor by uncommenting the line below.
#
# Replace D12 with D13 to use the red LED on the METRO board instead
# of an external LED.
#
# For the Pi Pico, use GP25 for the on-board green LED or any GP0-28 for an
# external LED.  Similarly, replace D2 with any GP0-28.
import board
import digitalio

led = digitalio.DigitalInOut(board.D12)
led.direction = digitalio.Direction.OUTPUT

switch = digitalio.DigitalInOut(board.D2)
switch.direction = digitalio.Direction.INPUT
#Uncomment the next line to pull up switch internally.
#switch.pull = digitalio.Pull.UP

while True:
    led.value = switch.value
