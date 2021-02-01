# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Periodically scan for devices connected to the
# built-in I2C interface using the following wiring:
#
#  QT BLACK => M4 GND
#  QT RED => M4 3.3V
#  QT BLUE => M4 SDA (serial data)
#  QT YELLOW => M4 SCL (serial clock)
#
# Any devices found are identified by their 7-bit ID in the
# range 0x08 - 0x77. The IDs for the I2C kit components are:
#
#  0x1c & 0x6a = 9 DoF IMU
#  0x39 = multi-spectrum sensor
#  0x3c = OLED display
#  0x77 = pressure sensor
#
import time
import board

i2c = board.I2C()
i2c.unlock()

print('Will scan I2C bus every second.')

while True:
    if i2c.try_lock():
        devices = i2c.scan()
        print(f'Found {len(devices)} devices: {[hex(id) for id in devices]}')
        i2c.unlock()
    time.sleep(1)
