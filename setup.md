# Initial Microcontroller Setup

The kit includes two METRO microcontroller boards that we refer to as "M4" and "Airlift".  The Airlift can be used as a regular M4, but has additional hardware to enable WiFi and Bluetooth communications.  There is also a Raspberry Pi Pico microcontroller board in each kit.

Each microcontroller contains two "firmware" programs: a bootloader (similar to a computer's BIOS program) and a main program (similar to computer's operating system kernel).

The traditional way of working with a microcontroller is to install a new main program (often written in C) every time you make a change to your firmware.  However, these devices are now capable enough to run a python interpreter, which enables simpler programming and allows you to focus more on design and less on software details. Therefore, the steps below install [CircuitPython](https://circuitpython.org/) as the main program.

The final piece of software you will need is an editor that works well with the CircuitPython development environment.  Unlike the bootloader and main program, which run on the M4, the editor runs on your computer and communicates with the M4 over USB.

The steps described below ensure that you have current working versions of these programs, and are based on the general instructions for the [M4 Express](https://circuitpython.org/board/metro_m4_express/), [M4 Airlift Lite](https://circuitpython.org/board/metro_m4_airlift_lite/) and [Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/).

## Instructions for January 2022

### Update the bootloader of both METRO boards to v.3.13.0

Connect the M4 to your computer via USB.  It should appear on your desktop as a new USB drive named **CIRCUITPY**.

On a Mac, the first time you insert a new M4 device, you may trigger the "Keyboard Setup Assistant" which attempts to configure a new USB keyboard. You can safely close the popup window and ignore this.

Double click the *Reset* button on the M4. The large round LED should turn green and **CIRCUITPY** will be renamed **METROM4BOOT**.  *You can safely ignore any warnings about the drive not being properly removed.*

Download the appropriate bootloader image to your computer then drag and drop it onto the **METROM4BOOT** USB drive:
 - [M4 Express](https://github.com/adafruit/uf2-samdx1/releases/download/v3.13.0/update-bootloader-metro_m4-v3.13.0.uf2)
 - [M4 Airlift Lite](https://github.com/adafruit/uf2-samdx1/releases/download/v3.13.0/update-bootloader-metro_m4_airlift-v3.13.0.uf2)
 - The Pico bootloader does not need updating.

The **METROM4BOOT** USB drive should disappear from your desktop then, after a delay of up to a minute, reappear.  Open the drive and check that the text file `INFO_UF2.TXT` contains either (M4 Express):
```
UF2 Bootloader v3.13.0 SFHWRO
Model: Metro M4 Express
Board-ID: SAMD51J19A-Metro-v0
```
or else (M4 Airlift Lite):
```
UF2 Bootloader v3.13.0 SFHWRO
Model: Metro M4 AirLift
Board-ID: SAMD51J19A-Metro-AirLift-v0
```
Remember to close `INFO_UF2.TXT` before you try to eject the **METROM4BOOT** USB drive.

You have now completed the METRO bootloader updates and are ready to install CircuitPython on your microcontroller boards.

### Update CircuitPython to 7.1.0

#### METRO Instructions

With your M4 mounted as **METROM4BOOT** (double click *Reset* if necessary), download the appropriate main program image and copy it to your M4:
 - [M4 Express](https://downloads.circuitpython.org/bin/metro_m4_express/en_US/adafruit-circuitpython-metro_m4_express-en_US-7.1.0.uf2)
 - [M4 Airlift Lite](https://downloads.circuitpython.org/bin/metro_m4_airlift_lite/en_US/adafruit-circuitpython-metro_m4_airlift_lite-en_US-7.1.0.uf2)

The **METROM4BOOT** USB drive should again disappear from your desktop and, after a short delay, reppear as **CIRCUITPY**.  Open the drive and check that the text file `boot_out.txt` contains either (for M4 Express):
```
Adafruit CircuitPython 7.1.0 on 2021-12-28; Adafruit Metro M4 Express with samd51j19
Board ID:metro_m4_express
```
or (for M4 Airlift Lite):
```
Adafruit CircuitPython 7.1.0 on 2021-12-28; Adafruit Metro M4 Airlift Lite with samd51j19
Board ID:metro_m4_airlift_lite
```

#### Pi Pico Instructions

The Pi Pico instructions are similar:
 - Connect your pico via USB and look for the **RPI-RP2** USB drive.
 - Download the [main program image](https://downloads.circuitpython.org/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-7.1.0.uf2)
 - Drag and drop this download onto the **RPI-RP2** USB drive.
 - After a short delay, you should see **RPI-RP2** replaced with **CIRCUITPY**.

Check that the `boot_out.txt` file contains:
 ```
Adafruit CircuitPython 7.1.0 on 2021-12-28; Raspberry Pi Pico with rp2040
Board ID:raspberry_pi_pico
```

You now have three microcontroller boards all called **CIRCUITPY** but you will not need to connect more than one at a time via USB.

#### Libraries

The `lib` folder on your **CIRCUITPY** drive contains python modules to support basic interaction with the M4 hardware.  Some of the components in your kit will require additional libraries to be installed later by copying them to this folder.  Instructions for that are [here](libraries.md).

You have completed your M4 setup and are ready to install a code editor.

### Install the Mu Editor

Any file named `code.py` on your **CIRCUITPY** drive will be automatically run whenever your M4 is reset.

In principle, you can use any text or code editor to modify `code.py` directly from the USB drive.  However,
we will start with the [Mu Editor](https://codewith.mu/) which is specifically designed to work well with Adafruit microcontroller boards and CircuitPython.

Visit this [download page](https://codewith.mu/en/download) to select the appropriate official installer for your computer.

The first time you run the Mu Editor, you will be prompted to select a [mode](https://codewith.mu/en/tutorials/1.0/modes): select the *Adafruit CircuitPython* mode (or, *CircuitPython* if that is not available).  Whenever you
are running Mu, you can view and change your mode by clicking on the *Mode*  button in the toolbar.

I recommend that everyone start with the Mu Editor.  However, if you prefer to use a different editor, start [here](https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code#1-use-an-editor-that-writes-out-the-file-completely-when-you-save-it-2977444-22).

You are now ready to starting programming your microcontroller boards.


## Instructions for January 2021

### Update the bootloader to v.3.10.0

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

### Update CircuitPython to 5.3.1

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

### Install the Mu Editor

Any file named `code.py` on your **CIRCUITPY** drive will be automatically run whenever your M4 is reset.

In principle, you can use any text or code editor to modify `code.py` directly from the USB drive.  However,
we will start with the [Mu Editor]() which is specifically designed to work well with Adafruit microcontroller boards and CircuitPython.

Visit this [download page](https://codewith.mu/en/download) to select the appropriate official installer for your computer.

**If you are using the latest "Catalina" version 11.x.x of MacOS, I recommend the ALPHA version instead of the official installer because of [this issue](https://github.com/mu-editor/mu/issues/1147).**

The first time you run the Mu Editor, you will be prompted to select a [mode](https://codewith.mu/en/tutorials/1.0/modes): select the *Adafruit CircuitPython* mode (or, *CircuitPython* if that is not available).  Whenever you
are running Mu, you can view and change your mode by clicking on the *Mode*  button in the toolbar.

I recommend that everyone start with the Mu Editor.  However, if you prefer to use a different editor, start [here](https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code#1-use-an-editor-that-writes-out-the-file-completely-when-you-save-it-2977444-22).

You are now ready to starting programming your M4 device.
