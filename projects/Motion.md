# Project: Motion Feedback

In this project, you will communicate with two different modules, using I2C and PWM protocols, to implement a visual motion feedback system:
 - the inertial measurement unit (IMU) will continuously measure the acceleration and magnetic field vectors, and
 - the 8-neopixel strip will provide real-time visual feedback to enable the circuit's user to align the IMU's y axis to be level with its y axis pointing north.

The instructions in this project are deliberately less detailed, now that you have more experience with building circuits and developing M4 code with the aid of [existing examples](../hello.md).

## Build the Circuit

You will need the following components:
 - M4
 - IMU
 - Neopixel strip
 - I2C cable
 - jumper wires
 - breadboard

We need the breadboard since there is only one 3.3V output available from the M4, but it must be connected to both the Neopixel strip and the I2C bus.

With your M4 disconnected (with no power), wire the IMU and neopixel strip to the breadboard, then use jumpers to connect the breadboard signals to the M4.  You will need to be able to rotate your IMU into different orientations later, so consider this as you select jumper wire lengths.  Also, think about chosing jumper wire colors that allow you to easily identify your power and ground.

Power the M4 via USB and check that the small green LED on the IMU is illuminated.  Open the Mu editor and verify that you can run a simple program to print a message every second.  If the M4 is not responding, disconnect the USB and check your wiring.

## Read out the Sensors

Write a program to read out the IMU's acceleration and magnetic field vectors and print their component values every 0.5 seconds.  Check that both vector magnitudes make sense when the IMU is at rest, i.e.
 - acceleration magnitude is around 9.8 m/s^2 (variations over the surface of the earth are less than 1%)
 - B field magnitude is 25-65 micro Teslas (look up a more precise expected value for your location on [this map that displays nanoTeslas](img/Bfield_strength.jpg))

Notice the diagram of the IMU's right-handed XYZ coordinate system printed on its silkscreen, which defines its local axes.

These sensor readings are fairly noisy so, next implement a loop to average 16 values and observe the improvement.  However, even with averaging the magnetic field measurements will still be noisy since the signal (the earth's magnetic field) is relatively weak.

Try moving the speaker from your kit close to the IMU and observe the effect of the small permanent magnet it contains on your measurements.  If the B field direction is far from where you think north should be, check for any nearby magnets (or large pieces of steel which will distort the magnetic field nearby).

In case your sensor values stop updating, there may be a problem with the locking of the I2C bus in the CircuitPython libraries, but power cycling (by disconnecting and reconnecting USB) should fix it.

## Calculate Angles

The visual feedback for this project is based on two angles that you can calculate from the acceleration and B field vectors:
 - **tilt**: the angle of the IMU y axis relative to "level", i.e. a plane tangent to the earth's surface.
 - **turn**: the angle of the IMU y axis relative to the component of the magnetic field in the IMU's x-y plane.

These calculations will require trig functions, which are available in the [math library](https://circuitpython.readthedocs.io/en/6.0.x/shared-bindings/math/index.html).  Most trig functions work in radians but you should convert your angles to degrees (and there is a `math` function for that).

Your angles should be in the 360-degree range (-180, +180) degrees, but the inverse trig functions `acos`, `asin` and `atan` return results only within a 180-degree range.  Therefore you will need to use the `atan2` function, documented [here](https://docs.python.org/3/library/math.html#math.atan2).

The sign of your angles should indicate which way to rotate the IMU in order to make its y axis level and pointing towards "north" (the magnetic field measures magnetic north, which is generally different from true north by an [angle that depends on your location](https://en.wikipedia.org/wiki/Magnetic_declination)):
 - tilt < 0 indicates that the +y end of the IMU should be raised.
 - turn < 0 indicates that the IMU should be rotated clockwise about its z axis (viewed from above).

Note that, using our definition of tilt, achieving zero tilt does not mean that the IMU x-y plane is horizontal.  Instead we only level the IMU's y axis since this simplifies the trig required and because the tilt of a plane is specified by two angles and so requires more complex visual feedback.

Update your code to calculate and display the tilt and turn values every 0.5 seconds.  Observe how the values change as you rotate the IMU and make sure the range and signs of your angles are correct before moving to the next section.

## Implement Visual Tilt Feedback

Update your program to provide visual feedback on the tilt angle following the top section of the guide below, where dark gray indicates that an LED is off and LEDs are numbered 0-7 from left to right. Use a brightness value of 0.05 to avoid any power consumption issues.  Note that the scheme we are using is intended to simulate the bubble in a traditional [spirit level](https://en.wikipedia.org/wiki/Spirit_level).  Ideally, we would combine the neopixel strip with the IMU in a package that keeps them rigidly connected and aligned, but in this prototype they move independently. However, the feedback you implement will make more sense if you keep them approximately aligned with each other.

Rotate your IMU and verify that only the 9 configurations in the guide are ever displayed and that they correspond to the printed tilt values.  I recommend using `auto_write=False` with `leds.show()` to prevent any intermediate states of the LEDs being displayed momentarily.

![Motion visual feedback scheme](https://raw.githubusercontent.com/dkirkby/E4S/main/projects/img/MotionFeedback.png)

## Implement Visual Turn Feedback

Comment out your code for visual tilt feedback and replace it with code for visual feedback on the turn angle, following the bottom section of the guide.

Rotate your IMU and verify that only the 9 configurations in the guide are ever displayed and that they correspond to the printed turn values.

## Implement Simultaneous Tilt and Turn Feedback

Finally, update your visual feedback code to overlay the tilt feedback on top of the turn feedback, i.e. with a white tilt pixel taking precedence over a background red/green/blue turn pixel. Notice how all 81  possible combinations of the individual turn and tilt feedbacks are still distinguishable after being overlayed like this, so we have not sacrificed any information with this scheme.

Rotate your IMU and verify that you now get it level and pointing north using only the visual feedback provided.

Define two boolean variables near the top of your program
```
TURN_FEEDBACK = True
TILT_FEEDBACK = True
```
and implement your code so that all 4 combinations of `True/False` work correctly.

Finally, remove the print statements and the timing delay from your main loop so your circuit provides more responsive feedback.
