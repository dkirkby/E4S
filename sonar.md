# Ultrasonic Sonar Distance Sensor

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

## Introduction

The general principle for measuring the distance to an object is to emit waves towards it then time how long it takes for a reflected wave to return.  The cheapest devices use ultrasound (at frequencies too high to hear), similar to medical imaging devices and bats.  More expensive devices use microwaves, as in a radar (RAdio Detection And Ranging), or an [infrared laser](https://www.adafruit.com/product/4058), as in lidar (LIght Detection And Ranging).

Discussion questions:
 - What are the advantages and disadvantages of using a shorter wavelength?
 - Why do you think that visible light is not used?

Your kit contains a cheap ultrasonic "sonar" (SOund NAvigation Ranging) device with a pair of similar looking devices, one of which transmits (labeled "T") and the other receives ("R").

## Test the Kit Device

Build the following circuit to experiment with your sonar sensor:

![sonar circuit](../img/sonar-circuit.jpg)

Like most sensors, it requires power (3.3V) and ground connections. The other two pins operate at digital levels and allow you to control the device.  The **Trig** pin is an input that triggers a new ultrasonic pulse to be emitted when it receives a short high pulse.  The **Echo** pin is an output that goes to a logic high level when the pulse is emitted then stays high until an echo is received (or a timeout occurs).  The distance is encoded in the duration of the **Echo** pulse, so requires precise timing of this duration.  CircuitPython provides a [library](https://github.com/adafruit/Adafruit_CircuitPython_HCSR04) to take care of this interfacing.

Enter the following program to test your device's capabilities:
```python
import time
import board
import adafruit_hcsr04

# See https://learn.adafruit.com/ultrasonic-sonar-distance-sensors/python-circuitpython
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP21, echo_pin=board.GP22)

# Average consecutive readings to reduce random noise.
# More averaging gives a slower but smoother response.
NAVG = 16

while True:
    distance = 0.
    nsamples = 0
    for i in range(NAVG):
        # The measurement will sometimes time out, resulting in a RuntimeError.
        # Therefore we cannot assume we will get NAVG samples and must count them.
        try:
            distance += sonar.distance
            nsamples += 1
        except RuntimeError:
            pass
    distance /= nsamples
    # Distances are nominally in centimeters.
    print((distance,))
    time.sleep(0.1)
```
Run this program and look at the Serial printed output to answer the following questions:
 - Over what range of distances is this device reasonably accurate for objects directly in front of the sensor?
 - How far off the central axis can the sensor "see" at a distance of 50cm?

Notice that the printed format is compatible with the Mu Plotter: open the Plot window to see a graph of distance versus time.  Try changing `NAVG` to 1 or 64 to see how it affects the performance.

## Exercise 1

Modify your circuit so that the Pico is also controlling the kit neopixel strip. *Hint: you will need to assign a dedicated Pico digital output for communicating with the strip.*

Modify your code so that the number of LEDs illuminated corresponds to the distance. *Hint: you will need to decide on the distance mininum and maximum distances corresponding to 0 or 8 LEDs illuminated, then linearly interpolate from the distance to the number of LEDs.*  The LED color is [up to you](https://www.rapidtables.com/web/color/RGB_Color.html).

## Exercise 2

Modify your code so that all the neopixel LEDs flash red if an object is detected closer than about 10cm, but are otherwise all off.

In order for this design to be useful, there needs to be a way to reset the alarm. For example, it could reset after some time delay (like most car alarms) or else require a switch to be pressed (like most house alarms).  Design, implement and test your own solution.
