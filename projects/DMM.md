# Project: Digital Multimeter

In this project, you will use your M4 board to create a simple digital multimeter (DMM).

Start by connecting a long black jumper wire to GND and a long red jumper wire to A0.

You can read the voltage on pin A0 using:
```
import time
import board
import analogio

A0 = analogio.AnalogIn(board.A0)

while True:
    ADU = A0.value
    print(f'ADU = {ADU:5d} (dec) = ${ADU:04x} (hex)')
    time.sleep(0.5)
```
Enter this program using the Mu editor and save to your M4 device. Open the "Serial" tab to display the resulting values.  If you are not familiar with [hexadecimal (hex) notation](https://www.youtube.com/watch?v=4EJay-6Bioo), take a moment to review it now.

With the black and red wires floating (i.e. not connected to anything at their other end), the printed values should be varying randomly.  However, they are not quite random: what pattern do you notice in the hex values?

The printed values are in "analog digital units" (ADU) so we still need to convert them to physical units.
To do this, connect the red wire to a different GND so we know the input is 0V.  Record the typical value you observe.  Note that we can leave the black wire floating since it already uses the same 0V (GND) reference as
the voltage source we are measuring (which is itself!)

Next, connect the red wire to 3.3V and record the typical value you observe.  Now write down a formula to
convert from ADUs to Volts, assuming a linear relationship.  Modify your code to print this value.

The `ADU` value is represented by 16 bits, so has a range from zero to `2^16-1` which equals 65,535 or $ffff in hex.  What do you expect would happen if you try to measure the 5V level on the M4?  Go ahead and try it.  Does
the result make sense?  (The A0 input has sufficient protection that 5V will not damage it, but a larger voltage could).

At this point, you have created a digital *voltmeter*.  To make this more of a *multimeter*, let's now add
resistance measurements.  Draw a [voltage divider circuit](https://learn.sparkfun.com/tutorials/voltage-dividers) with resistors R1 and R2 and write the equation for the voltage Vout between R1 and R2 when the circuit is powered by Vin=3.3V.  Next, assume that R1 (connected to 3.3V) is known, and write an equation for the unknown R2 (connected to GND) in terms of R1 and Vout.

Modify your circuit by adding R1=1K to the breadboard so that there are two long jumper wires that can be connected to the ends of an unknown resistance, forming a voltage divider whose output voltage is measured by A0. Adapt your code to print the value of the unknown resistance in Ohms.

Verify that your code is working by measuring all four of the resistors in your kit. Note that these resistors
have 1% "tolerance" which means that their true resistance is probably within 1% of their nominal value. Try some
parallel and series combinations of two resistors and check your measurements against calculated values.

To round out our multimeter, we should next add current measurements.  However, this is a bit trickier so
instead take a moment to think about how you might do this, and reflect on why multimeters always use
separate inputs to measure voltage (or resistance) and current.