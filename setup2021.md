# Setup Instructions for January 2021

## Update the bootloader to v.3.10.0

Connect the M4 to your computer via USB.  It should appear on your desktop as a new USB drive named **CIRCUITPY**.

On a Mac, the first time you insert a new M4 device, you may trigger the "Keyboard Setup Assistant" which attempts to configure a new USB keyboard. You can safely close the popup window and ignore this.

Double click the *Reset* button on the M4. The large round LED should turn green and **CIRCUITPY** will be renamed **METROM4BOOT**.  *You can safely ignore any warnings about the drive not being properly removed.*

Download the appropriate bootloader image to your computer then copy it to the **METROM4BOOT** USB drive:
 - [M4 Express](https://github.com/adafruit/uf2-samdx1/releases/download/v3.10.0/update-bootloader-metro_m4-v3.10.0.uf2)
 - [M4 Airlift Lite](https://github.com/adafruit/uf2-samdx1/releases/download/v3.10.0/update-bootloader-metro_m4_airlift-v3.10.0.uf2)

The **METROM4BOOT** USB drive should disappear from your desktop then, after about 5 seconds, reappear.  Open the drive and check that the text file `INFO_UF2.TXT` contains either (M4 Express):
```
UF2 Bootloader v3.10.0 SFHWRO
Model: Metro M4 Express
Board-ID: SAMD51J19A-Metro-v0
```
or else (M4 Airlift Lite):
```
UF2 Bootloader v3.10.0 SFHWRO
Model: Metro M4 AirLift
Board-ID: SAMD51J19A-Metro-AirLift-v0
```

You have now completed the bootloader update and are ready to install CircuitPython on your M4.

## Update CircuitPython to 5.3.1

Note that 5.3.1 is not the most recent version (6.0.1) since that currently has [some unresolved issues](https://github.com/adafruit/circuitpython/issues/3918).

With your M4 mounted as **METROM4BOOT** (double click *Reset* if necessary), download the appropriate main program image and copy it to your M4:
 - [M4 Express](https://adafruit-circuit-python.s3.amazonaws.com/bin/metro_m4_express/en_US/adafruit-circuitpython-metro_m4_express-en_US-5.3.1.uf2)
 - [M4 Airlift Lite](https://adafruit-circuit-python.s3.amazonaws.com/bin/metro_m4_airlift_lite/en_US/adafruit-circuitpython-metro_m4_airlift_lite-en_US-5.3.1.uf2)

The **METROM4BOOT** USB drive should again disappear from your desktop and, after a few seconds, reppear as **CIRCUITPY**.  Open the drive and check that the text file `boot_out.txt` contains either (for M4 Express):
```
Adafruit CircuitPython 5.3.1 on 2020-07-13; Adafruit Metro M4 Express with samd51j19
```
or (for M4 Airlift Lite):
```
Adafruit CircuitPython 5.3.1 on 2020-07-13; Adafruit Metro M4 Airlift Lite with samd51j19
```

The `lib` folder on your **CIRCUITPY** drive contains python modules to support basic interaction with the M4 hardware.  Some of the components in your kit will require additional libraries to be installed later by copying them to this folder.  Instructions for that are [here](libraries.md).

You have completed your M4 setup and are ready to install a code editor.

## Libraries

Some of the components in the kit need additional libraries that are not installed when you install CircuitPython. Any extra libraries needed are always mentioned in the comments at the top of each component's [hello example](hello.md).

To install an additional library, you just copy it into the `lib` folder of your CIRCUITPY usb drive. You only need to do this once.  The instructions below show you how to install all of the libraries for the kit components at once.

Since we are running CircuitPython 5.3.1, we need to install libraries from the 5.x bundle (we are using 5.x from the [20210101 release](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20210101)). We do not install the whole bundle since it is too big to fit in the M4.

Download and expand [this zip file](E4S-libaries-5.x.zip) with the libraries needed by the following kit components:
 - OLED display
 - pressure sensor
 - multi-spectrum light sensor
 - 9DoF inertial measurement unit

The expanded directory contains a mixture of folders and files with an `.mpy` extension.  Copy all of these into the `lib` folder on your the CIRCUITPY USB drive for each of your microcontroller boards.  Note that copying anything to CIRCUITPY (via the Mu editor or otherwise) causing any running program to be restarted.

You are now ready to use these libraries.

## Install the Mu Editor

You have completed the setup of your microcontroller boards and are now ready to install a code editor on your laptop.

Any file named `code.py` on your **CIRCUITPY** drive will be automatically run whenever your M4 is reset.

In principle, you can use any text or code editor to modify `code.py` directly from the USB drive.  However,
we will start with the [Mu Editor](https://codewith.mu/) which is specifically designed to work well with Adafruit microcontroller boards and CircuitPython.

Visit this [download page](https://codewith.mu/en/download) to select the appropriate official installer for your computer.

**If you are using the latest "Catalina" version 11.x.x of MacOS, I recommend the ALPHA version instead of the official installer because of [this issue](https://github.com/mu-editor/mu/issues/1147).**

The first time you run the Mu Editor, you will be prompted to select a [mode](https://codewith.mu/en/tutorials/1.0/modes): select the *Adafruit CircuitPython* mode (or, *CircuitPython* if that is not available).  Whenever you
are running Mu, you can view and change your mode by clicking on the *Mode*  button in the toolbar.

I recommend that everyone start with the Mu Editor.  However, if you prefer to use a different editor, start [here](https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code#1-use-an-editor-that-writes-out-the-file-completely-when-you-save-it-2977444-22).

You are now ready to starting programming your M4 device.
