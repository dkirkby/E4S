# Last Resort Recovery Procedure for Pico W

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

If a Pico W is not visible as a mounted USB drive (with any name) after plugging it in, and installing CircuitPython from BOOTSEL mode does not work (i.e. it still does not mount), then go back into BOOTSEL mode and copy [flash_nuke.uf2](bin/flash_nuke.uf2?raw=true) to the drive. It should then remount as **RPI-RP2** and you should be able to [install CircuitPython as usual](setup.md).

If these steps fail or you cannot get into BOOTSEL mode (where **RPI-RP2** is mounted), then your Pico W likely has an unrecoverable hardware problem.
