# E4S: Electronics for Scientists

Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and taught by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).

## Equipment

This course uses a [standard component kit](https://docs.google.com/spreadsheets/d/1fDZMHFTLSX1ApLEP1mGgGuPPSofG94EePxDg_fpRnkw/edit#gid=0) whose total cost is about US$200:

![Image of Kit Components](https://raw.githubusercontent.com/dkirkby/E4S/master/img/kit.jpg)

There are two components (9V supply, AC relay) that assume North American AC power.  The kit's jumper wires and cables are not shown in the photo.  If you are ordering components yourself, there is some soldering required to
attached headers.

Most of the components are designed and manufactured by [adafruit](https://www.adafruit.com/about) which provides excellent [supporting documentation and tutorials](https://learn.adafruit.com/).

The two microcontroller boards (Metro M4) are programmable and require some initial setup: instructions are [here](setup.md).

## Projects

1. [Digital Multimeter](projects/DMM.md)

## CircuitPython Libraries

Some of the components in the kit need additional [libaries to be installed](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries):

OLED display:
- adafruit_display_text
- adafruit_displayio_ssd1306
