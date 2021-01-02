# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Control an external LED connected to D12 using an
# external switch connected to D2, with an optional pullup.
import board
import digitalio

led = digitalio.DigitalInOut(board.D12)
led.direction = digitalio.Direction.OUTPUT

switch = digitalio.DigitalInOut(board.D2)
switch.direction = digitalio.Direction.INPUT
#Uncomment the next line to pull up D2 internally.
#switch.pull = digitalio.Pull.UP

while True:
    led.value = switch.value
