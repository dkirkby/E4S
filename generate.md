# Circuit Configuration Code

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

Most programs have the same basic structure:
 - imports
 - circuit configuration
 - infinite loop

Here is a basic example from [your first program](first_prog.md):
```python
import board
import digitalio
import time

led = digitalio.DigitalInOut(board.GP2)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = not led.value # toggle on/off
    time.sleep(0.5) # seconds
```

The circuit configuration is where you specify the connections between your Pico and the rest of the circuit. Each connection is either an Input or an Output. The voltage that you connect to is either being treated as Digital or Analog.

Use this [interactive tool](https://observablehq.com/embed/@dkirkby/pin-wizzard@63?cells=viewof+assign%2CgeneratedCode) to explore and generate code for the different options.
