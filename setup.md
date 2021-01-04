# Initial Microcontroller Setup

The kit includes two microcontrollers that we refer to as "M4" and "Airlift".  The Airlift can be used as a regular M4, but has additional hardware to enable WiFi and Bluetooth communications.

Each microcontroller contains two "firmware" programs: a bootloader (similar to a computer's BIOS program) and a main program (similar to computer's operating system kernel).

The traditional way of working with a microcontroller is to install a new main program (often written in C) every time you make a change to your firmware.  However, these devices are now capable enough to run a python interpreter, which enables simpler programming and allows you to focus more on design and less on software details. Therefore, the steps below install [CircuitPython](https://circuitpython.org/) as the main program.

The final piece of software you will need is an editor that works well with the CircuitPython development environment.  Unlike the bootloader and main program, which run on the M4, the editor runs on your computer and communicates with the M4 over USB.

The steps described below ensure that you have current working versions of these programs.  The general documentation for these steps is [here](https://circuitpython.org/board/metro_m4_express/) but you should normally follow one of the dated explicit recipes below.

## Instructions for 4 January 2021

### Update the bootloader to v.3.10.0

Connect the M4 to your computer via USB.  It should appear on your desktop as a new USB drive named **CIRCUITPY**.

Double click the *Reset* button on the M4. The large round LED should turn green and **CIRCUITPY** will be renamed **METROM4BOOT**.

Download [this file](https://github.com/adafruit/uf2-samdx1/releases/download/v3.10.0/update-bootloader-metro_m4-v3.10.0.uf2) then copy it to the **METROM4BOOT** USB drive.

The **METROM4BOOT** USB drive should disappear from your desktop then, after about 5 seconds, reappear.  Open the drive and check that the text file `INFO_UF2.TXT` contains:
```
UF2 Bootloader v3.10.0 SFHWRO
Model: Metro M4 Express
Board-ID: SAMD51J19A-Metro-v0
```


### Update CircuitPython to 5.3.1

Note that 5.3.1 is not the most recent version (6.0.1) since that currently has [some unresolved issues](https://github.com/adafruit/circuitpython/issues/3918).

With your M4 mounted as **METROM4BOOT** (double click *Reset* if necessary), download and copy [this file](https://adafruit-circuit-python.s3.amazonaws.com/bin/metro_m4_express/en_US/adafruit-circuitpython-metro_m4_express-en_US-5.3.1.uf2).

The **METROM4BOOT** USB drive should again disappear from your desktop and, after a few seconds, reppear as **CIRCUITPY**.  Open the drive and check that the text file `boot_out.txt` contains:
```
Adafruit CircuitPython 5.3.1 on 2020-07-13; Adafruit Metro M4 Express with samd51j19
```
The `lib` folder on your **CIRCUITPY** drive contains python modules to support basic interaction with the M4 hardware.  Some of the components in your kit will require additional libraries to be installed lateby copying them
to this folder.

The general documentation for installing CircuitPython is [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-circuitpython).


### Install the Mu Editor

Any file named `code.py` on your **CIRCUITPY** drive will be automatically run whenever your M4 is reset.

In principle, you can use any text or code editor to modify `code.py` directly from the USB drive.  However,
we will start with the [Mu Editor]() which is specifically designed to work well with Adafruit microcontroller boards and CircuitPython.

Visit this [download page](https://codewith.mu/en/download) to select the appropriate official installer for your computer.

**If you are using the latest "Catalina" version 11.x.x of MacOS, I recommend the ALPHA version instead of the official installer because of [this issue](https://github.com/mu-editor/mu/issues/1147).**

I recommend that everyone start with the Mu Editor.  However, if you prefer to use a different editor, start [here](https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code#1-use-an-editor-that-writes-out-the-file-completely-when-you-save-it-2977444-22).

The general instructions for installing the Mu Editor are [here](https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor).
