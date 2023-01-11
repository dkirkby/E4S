# Initial Microcontroller Setup

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

Each kit includes two Raspberry Pi Pico-W microcontroller boards. You will use these to bring your circuits to life with
some python programs that you write.  A microcontroller is a simple device that runs a single relatively simple program. It is not what you normally think of as a "computer", with an operating system or file system, unlike its bigger sister the [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/).

Each microcontroller contains two "firmware" programs: a bootloader (similar to a computer's BIOS program) and a main program (similar to computer's operating system kernel).  The traditional way of working with a microcontroller is to install a new main program (often written in C) every time you make a change to your code, using the bootloader.  However, these devices are now capable enough to run a python interpreter, which enables simpler programming and allows you to focus more on design and less on low-level details. Therefore, the steps below install [CircuitPython](https://circuitpython.org/) as the main program.

The final piece of software you will need is an editor that works well with the CircuitPython development environment.  Unlike the bootloader and main program, which run on the microcontroller, the editor runs on your computer and communicates with the microcontroller over USB.

The steps described below ensure that you have current working versions of these programs, and are based on the general instructions [here](https://circuitpython.org/board/raspberry_pi_pico_w/). These instructions were last updated in Jan 2023. For archived past instructions see [Jan 2022](setup2022.md) or [Jan 2021](setup2021.md).

## Install CircuitPython 8.0 on each Pico W

Download this [circuit python program](bin/adafruit-circuitpython-raspberry_pi_pico_w-en_US-8.0.0-beta.6.uf2?raw=true) to your laptop.  Since this program will run on the microcontroller, not your laptop, it does not matter what operating system your laptop is running.

Connect the Pico W to your laptop with a USB cable and look for a new USB drive called **RPI-RP2**.

> In case the Mac "Keyboard Setup Assistant" launches, just click "Quit" to close it.

> If your new USB drive is called **CIRCUITPYTHON** this means someone else has already done this installation, but perhaps for an older version. To reset your drive and continue with the instructions below, follow these steps:
 - unmount the **CIRCUITPYTHON** drive and uplug the USB from your laptop
 - press down the small white button while you plug the USB back into your laptop
 - you should now see the drive called **RPI-RP2** and can proceed with the steps below.

Copy the downloaded file to the USB drive, e.g. using drag and drop.  After a short while (10-20 secs) the **RPI-RP2** drive should be replaced with one called **CIRCUITPYTHON**.  This indicates that you have successfully installed the CircuitPython program on your microcontroller.

> Mac users will probably get a warning about "Disk Not Ejected Properly" that you can safely ignore.

If you open your **CIRCUITPYTHON** drive, you should see several files now, include a small text file `boot_out.txt` that starts with the lines:
```
Adafruit CircuitPython 8.0.0-beta.6 on 2022-12-21; Raspberry Pi Pico W with rp2040
Board ID:raspberry_pi_pico_w
```

Unmount your **CIRCUITPYTHON** drive the same way you would remove any USB drive, then repeat these steps for the other Pico W in your kit.

> Since both of your microcontrollers now have the same USB drive name, it would be confusing to have them both connected to your laptop at the same time.  However, while we will sometimes use both at once in a project, we will not need them both connected via USB at once.

## Libraries

Some of the components in the kit need additional libraries that are not installed when you install CircuitPython. Any extra libraries needed are always mentioned in the comments at the top of each component's [hello example](hello.md).

To install an additional library, you just copy it into a `lib` folder of your **CIRCUITPY** USB drive. You only need to do this once.  The instructions below show you how to install all of the libraries for the kit components at once.

Since we are running CircuitPython 8.0, we need to install libraries from the 8.x bundle (we are using 8.x from the [20230109 auto release](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/tag/20230109)). We do not install the whole bundle since it is too big to fit in the microcontroller memory.

Download and expand [this zip file](bin/E4S-libraries-8.x.zip?raw=true) with the libraries needed by the following kit components:
 - OLED display
 - pressure & altitude sensor
 - acceleration & rotation & magnetic field sensor
 - 10-band photodetector
 - ultrasonic distance sensor
 - Pico-W wifi networking

Open your **CIRCUITPY** USB drive and open the folder named `lib`, which should be empty if you just installed CircuitPython using the steps above. The expanded zip directory contains a mixture of folders and files with an `.mpy` extension.
Copy all of these into the `lib` folder on your the **CIRCUITPY** USB drive for each of your microcontroller boards.  Note that writing anything to **CIRCUITPY** will restart any program that is already running on the board.

You are now ready to use these libraries.

## Install the Mu Editor

You have completed the setup of your microcontroller boards and are now ready to install a code editor on your laptop.

Any file named `code.py` on your **CIRCUITPY** drive will be automatically run whenever your microcontroller is reset, either when you initially connect it via USB or when you press its reset button.

In principle, you can use any text or code editor to modify `code.py` directly from the USB drive.  However,
we will start with the [Mu Editor](https://codewith.mu/) which is specifically designed to work well with Adafruit microcontroller boards and CircuitPython.

Visit this [download page](https://codewith.mu/en/download) to select the appropriate official installer for your computer.

The first time you run the Mu Editor, you will be prompted to select a [mode](https://codewith.mu/en/tutorials/1.0/modes): select the *Adafruit CircuitPython* mode (or, *CircuitPython* if that is not available).  Whenever you are running Mu, you can view and change your mode by clicking on the *Mode*  button in the toolbar.

The name of the file you are currrently editing appears in the editor title bar, and should generally be `code.py`.  The first time you use the Mu Editor with a new **CIRCUITPY** drive installed, the name will be `untitled` and you will be prompted for a name: use `code.py`.

I recommend that everyone start with the Mu Editor.  However, if you prefer to use a different editor, start [here](https://learn.adafruit.com/welcome-to-circuitpython/creating-and-editing-code#1-use-an-editor-that-writes-out-the-file-completely-when-you-save-it-2977444-22).

You are now ready to [start programming your microcontroller boards](first-prog.md).
