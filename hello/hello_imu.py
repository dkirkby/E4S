# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Read inertial motion parameters from the LSM6DS + LIS3MDL
# connected via the built-in I2C interface.
#
# The following files must be copied to your CIRCUITPY lib/ folder:
#
#  adafruit_lis3mdl.mpy
#  adafruit_lsm_6ds/*
#  adafruit_register/*
#
# For details see https://learn.adafruit.com/adafruit-lsm6ds3tr-c-lis3mdl-precision-9-dof-imu/python-circuitpython
#
# Connect the QT-pin cable to the IMU and wire to the M4:
# BLACK => GND
# RED => 3.3V
# BLUE => SDA (serial data)
# YELLOW => SCL (serial clock)
import time
import math

import board
import busio

try:
    # SDA, SCL are predefined on M4
    sda, scl = board.SDA, board.SCL
except:
    # Use SDA=GP0, SCL=GP1 on Pico
    sda, scl = board.GP0, board.GP1

i2c = busio.I2C(sda=sda, scl=scl)

# These files are not in the base CircuitPython installation.
# See instructions above for installing them and their dependencies.
import adafruit_lis3mdl
import adafruit_lsm6ds.lsm6ds3

bsens = adafruit_lis3mdl.LIS3MDL(i2c)
imu = adafruit_lsm6ds.lsm6ds3.LSM6DS3(i2c)

def magnitude(vec):
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1] + vec[2] * vec[2])

while True:
    # Read the magnetic field strength vector in micro Teslas.
    bfield = bsens.magnetic
    # Calculate the magnitude of the B field which should be about 47 uT in Irvine.
    bmag = magnitude(bfield)
    print(f'B=({bfield[0]:.2f},{bfield[1]:.2f},{bfield[2]:.2f}) |B|={bmag} uT')
    # Read acceleration vector in m/s^2.
    accel = imu.acceleration
    # Calculate the magnitude of the acceleration vector which should be 9.81 m/s^2 at rest.
    amag = magnitude(accel)
    print(f'accel=({accel[0]:.2f},{accel[1]:.2f},{accel[2]:.2f}) |a|={amag:.2f} m/s^2')
    # Read angular velocity vector in rad/s which should be ~0 at rest.
    gyro = imu.gyro
    # Convert from rad/s to deg/s.
    gdeg = [math.degrees(g) for g in gyro]
    gmag = magnitude(gdeg)
    print(f'omega=({gdeg[0]:.1f},{gdeg[1]:.1f},{gdeg[2]:.1f}) |omega|={gmag:.1f} deg/s')
    time.sleep(1)
