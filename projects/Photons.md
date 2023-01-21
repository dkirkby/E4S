# Project: Waveforms and Photons

In this project, you will generate and monitor analog waveforms to control photons produced by a light-emitting diode (LED).

## Analog Waveform Output

Build the circuit shown below with your microcontroller, a pair of 10KΩ resistors, a 1μF capacitor, your breadboard and some jumper wires:

![Voltage divider circuit](../img/voltage-divider-photo.jpg)

The corresponding schematic diagram is:

![Voltage divider schematic](../img/voltage-divider-diag.jpg)

This is another voltage divider but with a capacitor added. The purpose of the capacitor is to smooth the PWM output from **GP22* by shunting frequencies above 1/RC ~ 100 Hz to ground instead of the ADC input.

Use the following program to test this circuit:
```python
import time
import board
import analogio
import pwmio

PWM = pwmio.PWMOut(board.GP22, frequency=1000)
ADC = analogio.AnalogIn(board.A0)

# Print numeric values in the format required for the Mu Plotter.
# See https://codewith.mu/en/tutorials/1.2/plotter for details.
def printForMuPlotter(*values, intFormat='{value:05d}', floatFormat='{value:+.3f}'):
    formatted = [
        intFormat.format(value=value) if isinstance(value, int) else floatFormat.format(value=value)
        for value in values
    ]
    print(f'({",".join(formatted)})')

# Set an analog output level using PWM and read an ADC analog input level with averaging.
def measure(outputLevel, numAverage=128, delay=0.001, PWM=PWM, ADC=ADC):
    # Set the output level.
    PWM.duty_cycle = outputLevel
    inputLevel = 0.0
    for sample in range(numAverage):
        time.sleep(delay)
        inputLevel += ADC.value
    return max(round(inputLevel / numAverage), 0)

# Parameters defining the output sawtooth waveform.
LO = 0x0000
HI = 0xffff
STEP = 0x0600

# Set the initial output level.
ADUin = LO
while True:
    # Set the output level and read the corresponding input level.
    ADUout = measure(ADUin)
    # Print the result for the Mu Plotter.
    printForMuPlotter(ADUin, ADUout)
    # Update the output level.
    ADUin += STEP
    if ADUin > HI:
        ADUin = LO
```
We are using two utility functions here: `printForMuPlotter` and `measure`.  The comments describe
their purpose, but you don't need to understand the details of how they are implemented. Values in the code starting with `0x` are integers specified in [hexadecimal notation](https://en.wikipedia.org/wiki/Hexadecimal), which is convenient for the 16-bit unsigned values used to set and read analog levels here.

Download your program and click on the **Serial** icon in the Mu editor toolbar: you should see a stream of numbers being printed, using the
[python tuple](https://docs.python.org/3.8/library/stdtypes.html#tuple) format which is required for the [Mu Plotter](https://codewith.mu/en/tutorials/1.2/plotter).

Next, click on the **Plotter** icon in the Mu editor toolbar to display a real-time graph of these values, which should look something like this:

![Voltage divider ADU curves](../img/voltage-divider-adu-curves.jpg)

Does the relationship between the graphs of A0 and A1 (displayed in ADU units) make sense in terms of the circuit?

The Mu Plotter is very convenient but not very flexible.  For example, you cannot set the vertical range. You can drag the borders between the Mu editor panels to give the graph more space.  You have now created
a crude (and slow) [function generator](https://en.wikipedia.org/wiki/Function_generator) and [oscilloscope](https://en.wikipedia.org/wiki/Oscilloscope) for under $10!

## A Non-linear Circuit

Replace the 10KΩ resistor connected to ground with the red LED, whose datasheet is
[here](../datasheets/LED.pdf). Your LED should now be emitting light during part of the cycle.  If not, try turning it around (the shorter leg of the LED should be connected to ground).

Notice how the displayed ADUout waveform has changed with the LED replacing one of the resistors.  The relationship between ADUin and ADUout is now *non-linear*, i.e. we cannot write a linear equation for Vout in terms of Vin
that is valid throughout the cycle.  This is because diodes are non-linear devices, like transistors (which are basically a pair of diodes) and unlike resistors and capacitors.

There are two distinct phases to each cycle: describe them.  How is the LED emission different in each phase?
The roughly constant voltage across the diode during the second phase is referred to as the *Forward Voltage* in the datasheet, and is also known as the "diode drop".  Refer to Figure 1 in the datasheet to see that the
forward voltage is not actually constant, but depends on the forward current flowing through the LED.

Write an equation for the forward current `iLED` flowing through the LED in terms of the voltages Vin (at pin **GP22**) and Vout (at pin **ADC0**), both in Volts, and the known resistance R in Ohms. You can assume a slowly varying signal for this calculation, which means you can ignore the capacitor so that the LED current equals the current through the 10KΩ resistor.

Modify your code to calculate and this current `iLED` in units of 0.1 mA (these strange units are required for plotting voltages and current on the same scale).  You can use the following conversion from ADU to volts (where we are neglecting the small offset you measured in the [DMM Project](DMM.md)):
```python
    Vin = ADUin * 3.3 / 0xffff
    Vout = ADUout * 3.3 / 0xffff
```
Note the use of hexadecimal again: `0xffff` equals the maximum possible (unsigned) 16-bit value of $$2^16 - 1 = 65,535$$.

Modify your code to plot `Vin`, `Vout` and `iLED` using:
```python
    #printForMuPlotter(ADUin, ADUout)
    printForMuPlotter(Vin, Vout, iLED)
```
You should see something like this:

![LED voltage and current](../img/led-curves.jpg)

The curves of `Vin` and `Vout` are similar to the earlier curves for `ADUin` and `ADUout` but rescaled from ADU to Volts.  If you get a different `iLED` curve, check your calculation of the current and that you have converted to 0.1 mA units.

## A Pulsing LED

Our next goal is to control photon emission from the LED, but this only occurs during the second phase of the cycle.
To restrict our cycle to the second phase, we need to find a suitable value of the `LO` variable corresponding to when the LED current first starts its linear increase.  Modify your code to print values of `ADUin` and `iLED` using:
```python
    #printForMuPlotter(ADUin, ADUout)
    #printForMuPlotter(Vin, Vout, iLED)
    printForMuPlotter(ADUin, iLED)
```
Close the Plotter and open the Serial pane to see the numerical values. To print just one cycle, add a `break` statement:
```python
    if ADUin > HI:
        break
        ADUin = LO
```
Look through the printed table of `ADUin` and `iLED` values to find a suitable value of `LO` where `iLED` starts its linear increase. You will get slightly different values each time you run this program, so the uncertainty in your `LO` will probably be about ±500.  Check that when you use this value of `LO` in your code (instead of the orignal value of `0x0000`) there is no part of the cycle where the LED is dark, although it will start out very faint.  Remember to remove the `break` to restore the cycles.

Finally, modify your loop to modulate the LED brightness with a smooth sine function with a period of about 5 seconds, similar to the glowing logo on some laptops.  To accomplish this, you will need to replace the sawtooth ramp of `ADUin` with a sinusoidal variation of `ADUin` between the limits of `LO` and `HI`.  Python has a [sine function](https://docs.python.org/3/library/math.html#math.sin) you can use, but you need to `import math` to access it. Note that the python trig functions all expect their input angles in radians.

## Photon Control

Your design is now directly controlling the forward current flowing through the LED.  Next, you will estimate the corresponding rate of photons entering your eye...

Modify your code so that a constant forward current of 0.1mA flows through the LED.  Go back to the printed table of `ADUin` and `iLED` values to determine an ADU value `ON` that corresponds approximately to 0.1mA (remembering that `iLED` is in units of 0.1mA!)

In your program's main loop, toggle a 0.1mA LED current on and off, once per second, using:
```python
while True:
    ADUout = measure(ON)
    time.sleep(0.5)
    ADUout = measure(LO)
    time.sleep(0.5)
```
Check that this indeed blinks the LED once per second.

Calculate the number of electrons passing through the LED per second at 0.1mA. Each electron has some probability to be converted into a photon leaving the LED known as the **quantum efficiency**.  The datasheet does not provide this value, so we will assume it is 1%.

Next, assume that your pupil is a circle of 5mm diameter, and calculate the fraction of photons entering your
eye from an LED 1 meter away that emits *isotropically*, i.e. with equal intensity in all directions. How would
this fraction change if the distance was increase by a factor of two?

Observe the LED from directly overhead (the "north pole") then at a 90 degree angle (the "equator") and notice that the actual LED emission is far from isotropic. The LED body, viewed from above, is not round but elliptical, as shown on page 9 of the datasheet.  Is the brightness along the equator different when you look at the short or axis of this ellipse?

Figure 6 of the datasheet shows the LED's **field pattern** of relative luminous intensity (brightness) for different viewing angles.  An accurate calculation of the photon rate into your eye would need to model and  account for these field angle effects.  Instead, we will simply assume that a viewing angle of 80 degrees, close to the equator and looking toward the long axis of the ellipse, results in a factor of 10 reduction in the photon rate relative to an isotropic emitter.

Figure 5 of the datasheet shows that the LED photons are emitted within a narrow range of wavelengths centered
around 620 nanometers (nm).

Combine the factors above to estimate the rate of 620nm photons entering your eye, per second, at an 80 degree viewing angle, as a function of distance from the LED in meters.  Assume that the LED is always on for the purposes of this calculation, i.e. you do not need to account for the on/off toggle. Modify your program to calculate and print the rates at 2,4,6,...,40 meters (even values only).

Find a dark location and determine the distance at which you can just barely detect the blinking LED with your eye.  What is your corresponding detection threshold rate in photons per second?  Note that the human eye can detect single photons under [special conditions](https://en.wikipedia.org/wiki/Absolute_threshold#Vision) but your experiment will likely be limited by the ambient light levels.
