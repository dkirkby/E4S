# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Blink an external LED connected to D12.
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.D12)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = not led.value # toggle on/off
    time.sleep(0.5) # seconds
