# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Periodically scan for devices connected to the
# built-in I2C interface using the following wiring:
#
#  QT BLACK => M4 GND
#  QT RED => M4 3.3V
#  QT BLUE => M4 SDA or Pico GP0 (serial data)
#  QT YELLOW => M4 SCL or Pico GP1 (serial clock)
#
# Any devices found are identified by their 7-bit ID in the
# range 0x08 - 0x77. The IDs for the I2C kit components are:
#
#  0x1c = acceleration & rotation sensor (on same IMU as 0x6a)
#  0x6a = magnetic field sensor (on same IMU as 0x1c)
#  0x39 = 10-band photodetector
#  0x3c = OLED display
#  0x77 = pressure & altitude sensor
#
# The M4 has fixed pins with hardware support for the I2C protocol,
# but the Pico is more flexible due to its PIO hardware.
# Change GP0,GP1 below to use different pins on a Pico board.
import time
import board
import busio

try:
    # SDA, SCL are predefined on M4
    sda, scl = board.SDA, board.SCL
except:
    # Use SDA=GP0, SCL=GP1 on Pico
    sda, scl = board.GP0, board.GP1

i2c = busio.I2C(sda=sda, scl=scl)
i2c.unlock()

print('Will scan I2C bus every second.')

while True:
    if i2c.try_lock():
        devices = i2c.scan()
        print(f'Found {len(devices)} devices: {[hex(id) for id in devices]}')
        i2c.unlock()
    time.sleep(1)
