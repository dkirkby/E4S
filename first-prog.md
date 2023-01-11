# Your First Circuit and Program

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

Build the circuit below using a Pico W microcontroller (not yet connected to your laptop via USB), a 1KΩ resistor, a red or green LED (your choice), your breadboard and some jumper wires:

![First circuit construction](img/first-circuit.jpg)

Note that an LED is directional, i.e. does not work the same way forwards and backwards. This means you need to insert it into your breadboard with the correct orientation.  Don't worry if you get this wrong since it will do any damage. In this case, the longer wire on the LED should be connected to the resistor (through a hidden breadboard wire).

The corresponding electrical diagram is:

![First circuit diagram](img/first-circuit-diagram.png)

The light-green microcontroller pins labeled **GP2, GP3, GP4, ...* are for general-purpose digital input and output. In this context, *digital* means that signals are represented by a voltage that is either close to 0V ("low") or close to 3.3V ("high").
To complete your circuit, connect the Pico W to your laptop with a USB cable.  This will apply power to your circuit (from your laptop's USB port) and start running any previously loaded program, but there probably won't be any sign of this.

To bring this circuit to life, enter the following program into your Mu editor:
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
To load this program into the RP2020 processor on your Pico W board, you simply save it in the Mu editor.  This triggers the Mu editor to download your program via the USB cable and reset the processor so it starts running your code.  If all goes well, you should now see your LED blinking once per second.

Here are some experiments to try with your circuit and code. For each one, predict what might happen, try it then, in case you are surprised, think about why:
 - Remove the resistor
 - Turn the LED around
 - Change the 0.5 second delay to something much smaller or bigger
 - Use a different GND pin on the Pico W
 - Use a different GPn pin on the Pico W (can you modify your code to make this work?)
 - Unmount the **CIRCUITPY** USB drive from your laptop and plug it into a USB charger
