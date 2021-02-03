# CircuitPython Libraries

Some of the components in the kit need additional libraries that are not installed when you install CircuitPython following [these steps](setup.md).

Any extra libraries needed are always mentioned in the comments at the top of each component's [hello example](hello.md).

To install an additional library, you just copy it into the `lib` folder of your CIRCUITPY usb drive. You only need to do this once.  The instructions below show you how to install all of the libraries for the kit components at once.

## Instructions for January 2021

Since we are running CircuitPython 5.3.1, we need to install libraries from the 5.x bundle. We do not install the whole bundle since it is too big to fit in the M4.

Download and expand [this zip file](E4S-libaries-5.x.zip) with the libraries needed by the following kit components:
 - OLED display
 - pressure sensor
 - multi-spectrum light sensor
 - 9DoF inertial measurement unit

The expanded directory contains a mixture of folders and files with an `.mpy` extension.  Copy all of these into the `lib` folder on your CIRCUITPY usb drive.  Note that copying anything to CIRCUITPY (via the Mu editor or otherwise) causing any running program to be restarted.

You are now ready to use these libraries.
