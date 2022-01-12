# Initial Microcontroller Setup

The kit includes two METRO microcontroller boards that we refer to as "M4" and "Airlift".  The Airlift can be used as a regular M4, but has additional hardware to enable WiFi and Bluetooth communications.  There is also a Raspberry Pi Pico microcontroller board in each kit.

Each microcontroller contains two "firmware" programs: a bootloader (similar to a computer's BIOS program) and a main program (similar to computer's operating system kernel).

The traditional way of working with a microcontroller is to install a new main program (often written in C) every time you make a change to your firmware.  However, these devices are now capable enough to run a python interpreter, which enables simpler programming and allows you to focus more on design and less on software details. Therefore, the steps below install [CircuitPython](https://circuitpython.org/) as the main program.

The final piece of software you will need is an editor that works well with the CircuitPython development environment.  Unlike the bootloader and main program, which run on the M4, the editor runs on your computer and communicates with the M4 over USB.

The steps described below ensure that you have current working versions of these programs, and are based on the general instructions for the [M4 Express](https://circuitpython.org/board/metro_m4_express/), [M4 Airlift Lite](https://circuitpython.org/board/metro_m4_airlift_lite/) and [Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/).

These instructions were last updated in Jan 2022. Instructions for Jan 2021 are archived [here](setup2021.md).

## Update the bootloader of both METRO boards to v.3.13.0

Connect the M4 to your computer via USB.  It should appear on your desktop as a new USB drive.

On a Mac, the first time you insert a new M4 device, you may trigger the "Keyboard Setup Assistant" which attempts to configure a new USB keyboard. You can safely close the popup window and ignore this.

If the drive is named **CIRCUITPY**, open it and delete all the files it contains (e.g. by dragging them to the trash).  Next, double click the *Reset* button on the M4. The large round LED should turn green and **CIRCUITPY** will be renamed **METROM4BOOT**.  *You can safely ignore any warnings about the drive not being properly removed.*

If the drive is already named **METROM4BOOT** you can skip the delete and double click steps above.

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

## Update CircuitPython to 7.1.0

### METRO Instructions

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
If you deleted all the files on your M4 before installing CircuitPython, `boot_out.txt` will be the only file you see now.

### Pi Pico Instructions

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

You now have three microcontroller boards, all called **CIRCUITPY**, but you will not need to connect more than one at a time via USB.

## Libraries

Some of the components in the kit need additional libraries that are not installed when you install CircuitPython. Any extra libraries needed are always mentioned in the comments at the top of each component's [hello example](hello.md).

To install an additional library, you just copy it into a `lib` folder of your **CIRCUITPY** USB drive. You only need to do this once.  The instructions below show you how to install all of the libraries for the kit components at once.

Since we are running CircuitPython 7.1.0, we need to install libraries from the 7.x bundle (we are using 7.x from the [20220105 release](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20220105)). We do not install the whole bundle since it is too big to fit in the microcontroller memory.

Download and expand [this zip file](E4S-libraries-7.x.zip?raw=true) with the libraries needed by the following kit components:
 - OLED display
 - pressure sensor
 - multi-spectrum light sensor
 - 9DoF inertial measurement unit

Open your **CIRCUITPY** USB drive and create an empty folder named `lib`. (If you did not delete
files earlier, you may already have a `lib` folder). The expanded zip directory contains a mixture of folders and files with an `.mpy` extension.
Copy all of these into the `lib` folder on your the **CIRCUITPY** USB drive for each of your microcontroller boards.  Note that writing anything to **CIRCUITPY** will restart any program that is already running on the board.

You are now ready to use these libraries.

## Install the Mu Editor

You have completed the setup of your microcontroller boards and are now ready to install a code editor on your laptop.

Any file named `code.py` on your **CIRCUITPY** drive will be automatically run whenever your M4 is reset.

In principle, you can use any text or code editor to modify `code.py` directly from the USB drive.  However,
we will start with the [Mu Editor](https://codewith.mu/) which is specifically designed to work well with Adafruit microcontroller boards and CircuitPython.

Visit this [download page](https://codewith.mu/en/download) to select the appropriate official installer for your computer.

The first time you run the Mu Editor, you will be prompted to select a [mode](https://codewith.mu/en/tutorials/1.0/modes): select the *Adafruit CircuitPython* mode (or, *CircuitPython* if that is not available).  Whenever you are running Mu, you can view and change your mode by clicking on the *Mode*  button in the toolbar.

The name of the file you are currrently editing appears in the editor title bar, and should generally be `code.py`.  The first time you use the Mu Editor with a new **CIRCUITPY** drive installed, the name will be `untitled` and you will be prompted for a name: use `code.py`.

I recommend that everyone start with the Mu Editor.  However, if you prefer to use a different editor, start [here](https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code#1-use-an-editor-that-writes-out-the-file-completely-when-you-save-it-2977444-22).

You are now ready to starting programming your microcontroller boards.
