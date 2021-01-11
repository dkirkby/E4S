# Project: Photons

In this project, you will generate and monitor analog waveforms to control photons produced by a light-emitting diode (LED).

The schematics for this circuit are below:
![Project Schematics](https://raw.githubusercontent.com/dkirkby/E4S/master/projects/img/photons.png)

## Analog Waveform Output

Construct schematic 1 and enter the following program to drive the M4 A0 pin with a "sawtooth" waveform:
```
import time
import board
import analogio

A0 = analogio.AnalogOut(board.A0)

LO = 0x0000
HI = 0xffff
STEP = 0x0600

ADU0 = LO

while True:
    A0.value = ADU0
    print((ADU0,))
    time.sleep(0.05)
    ADU0 += STEP
    if ADU0 > HI:
        ADU0 = LO
```
Download your program and click on the **Serial** icon in the Mu editor toolbar: you should see a stream of numbers being printed, using the
[python tuple](https://docs.python.org/3.8/library/stdtypes.html#tuple) format `(1234,)`.

Click on the **Plotter** icon in the Mu editor toolbar to display a real-time graph of these values.
You can drag the borders between the Mu editor panels to give the graph more space.  You have now created
a crude (and slow) [function generator](https://en.wikipedia.org/wiki/Function_generator).

Details on the Mu editor plotter are [here](https://codewith.mu/en/tutorials/1.0/plotter): it is very convenient but not very flexible.  For example, the vertical range is always centered on zero even though our waveform is always positive.  The displayed values also suffer from random ADC noise, resulting in a slightly jagged waveform, and the plotter sometimes misses printed values, resulting in a compressed horizontal axis.

## Analog Waveform Input

Connect a jumper wire to the M4 A1 as shown in schematic 2.  Modify your code to configure A1 for analog input, then read and display its value within the loop (changes are indicated with comments):
```
import time
import board
import analogio

A0 = analogio.AnalogOut(board.A0)
A1 = analogio.AnalogIn(board.A1)   # new

LO = 0x0000
HI = 0xffff
STEP = 0x0600

ADU0 = LO

while True:
    A0.value = ADU0
    ADU1 = A1.value                # new
    print((ADU0,ADU1))             # edited
    time.sleep(0.05)
    ADU0 += STEP
    if ADU0 > HI:
        ADU0 = LO
```
After downloading your updated code, you should now see two waveforms displayed.  Does the relationship between
the graphs of A0 and A1 (displayed in ADU units) make sense in terms of the circuit?

You have now added basic [oscilloscope](https://en.wikipedia.org/wiki/Oscilloscope) functionality to your design.

## A Non-linear Circuit

Replace the 1K resistor connected to ground with the red LED, whose datasheet is
[here](https://github.com/dkirkby/E4S/raw/main/datasheets/LED.pdf). Your LED should now be emitting light during part of the cycle.  If not, try turning it around (the short leg of the LED should be connected to ground).

Notice how the displayed A1 waveform has changed with the LED replacing one of the resistors.  The relationship between ADU0 and ADU1 is now *non-linear*, i.e. we cannot write a linear equation for ADU1 in terms of ADU0
that is valid throughout the cycle.  This is because diodes are non-linear devices, like transistors (which are basically a pair of diodes) and unlike resistors and capacitors.

There are two distinct phases to each cycle: describe them.  How is the LED emission different in each phase?
The roughly constant voltage across the diode during the second phase is referred to as the *Forward Voltage* in the datasheet, and is also known as the "diode drop".  Refer to Figure 1 in the datasheet to see that the
forward voltage is not actually constant, but depends on the forward current flowing through the LED.

Write an equation for the forward current `iLED` flowing through the LED in terms of the voltages V0 at A0 and V1 at A1, and the known resistance R.  Modify your code to calculate and this current in milliamps (mA).  You can use the following conversion from ADU to volts (where we are neglecting the small offset you measured in the [DMM Project](DMM.md)):
```
    V0 = ADU0 * 3.3 / 0xffff
    V1 = ADU1 * 3.3 / 0xffff
```
Modify your code to print `V0` and `iLED` for display in the plotter:
```
    print((V0,iLED,))
```

## Startup Calibration

Our goal in this project is to control photon emission, but this only occurs during the second phase of the cycle.
To restrict our cycle to the second phase, we need to find a suitable value of the `LO` variable.  Try some different values in your code to get a rough estimate of where the forward current first becomes non-zero, resulting in some light emission.

We could manually calibrate this circuit and hardcode the resulting `LO` value, but this is not a very good design since it only works for your particular circuit, and might not even work well tomorrow when the temperature is different.  Alternatively, you could pay for more expensive resistors and LEDs with factory calibrated parameters so that different circuits would have similar calibrations.  However, the best solution is generally to use uncalibrated (cheap) components and then leverage the processing power of your design to implement a self-calibration sequence at start up (power on or system reset).

To do this, add the following skeleton functions to the top of your code:
```
...
A0 = analogio.AnalogOut(board.A0)
A1 = analogio.AnalogIn(board.A1)

def measure(ADU0, n=512):
    """Output the value ADU0 on A0 then read A1 n times
    and return the average A0-A1 difference in ADU."""
    return 0

def calibrate(y0=0, x1=0xb000, x2=0xffff):
    """Measure y1 at x1 and y2 at x2 then return the value x0
    where y(x0)=y0 for the straight line function y(x) passing
    through (x1,y1) and (x2,y2).
    """
    return 0

LO = round(calibrate())
HI = 0xffff
STEP = 0x0600
...
```
Next, read the comments and implement these functions and download your code. Notice how we perform many repeated analog measurements to reduce the effects of random noise.

When these functions are implemented correctly, you should see the graph of `iLED` increase (approximately) linearly from zero on each cycle with corresponding brightness variations in the LED.  There should no longer be an initial part of the cycle when the LED is off.

## A Different Function: Apple Power

Modify your loop to modulate the LED brightness using a smooth sine function with a period of about 5 seconds, similar to the glowing logo on some laptops.  Remove the `print` and `time.sleep` statements from your code and watch the LED to fine tune your code.  You will need to `import math` to evaluate the sine function.

## Photon Control

Your design is now directly controlling the forward current flowing through the LED.  Next, you will estimate the corresponding rate of photons entering your eye...

Modify your code so that a constant forward current of 0.1mA flows through the LED.  Hint: you can do this by passing a value of `y0 = ADU0-ADU1` to `calibrate()` that is different from the default `y0 = 0`.  Use the
resulting value in ADU to set A0 for the desired LED current.

Calculate the number of electrons passing through the LED per second at 0.1mA. Each electron has some probability to be converted into a photon leaving the LED known as the **quantum efficiency**.  The datasheet does not provide this value, so we will assume it is 1%.

Next, assume that your pupil is a circle of 5mm diameter, and calculate the fraction of photons entering your
eye from an LED 1 meter away that emits *isotropically*, i.e. with equal intensity in all directions. How would
this fraction change if the distance was increase by a factor of two?

Observe the LED from directly overhead (the "north pole") then at a 90 degree angle (the "equator") and notice that the actual LED emission is far from isotropic. The LED body, viewed from above, is not round but elliptical, as shown on page 9 of the datasheet.  Is the brightness along the equator different when you look at the short or axis of this ellipse?

Figure 6 of the datasheet shows the LED's **field pattern** of relative luminous intensity (brightness) for different viewing angles.  An accurate calculation of the photon rate into your eye would need to model and  account for these field angle effects.  Instead, we will simply assume that viewing angle of 80 degrees, close to the equator and looking toward the short axis of the ellipse, results in a factor of 10 reduction in the photon rate relative to an isotropic emitter.

Figure 5 of the datasheet shows that the LED photons are emitted within a narrow range of wavelengths centered
around 620 nanometers (nm).

Combine the factors above to estimate the rate of 620nm photons entering your eye, per second, at an 80 degree viewing angle, as a function of distance from the LED in meters.  Modify your program to print the rates
at 1,2,3,...,20 meters.

Find a dark location and determine the distance at which you can just barely detect any photons with your eye.  What is your corresponding threshold rate in photons per second?
