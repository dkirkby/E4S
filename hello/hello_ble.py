# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate communication over low-energy bluetooth (BLE) with
# the Metro M4 airlift's on-board ESP32.
#
# The libraries needed to communicate with the ESP32 in this
# example should already be included with the M4 Airlift
# CircuitPython installation.
#
# For more details, see
# https://learn.adafruit.com/adafruit-metro-m4-express-airlift-wifi/circuitpython-ble
#
# No wiring is required.
import board

try:
    # These libraries should be installed in the M4 airlift lib/ folder
    from adafruit_ble import BLERadio
    from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
    from adafruit_ble.services.nordic import UARTService
    from adafruit_airlift.esp32 import ESP32
except ImportError as e:
    print(e)
    print('Are you running on an M4 Airlift?')
    while True: pass

# Initialize a connection to the ESP coprocessor over SPI.
esp32 = ESP32()

# Start bluetooth.
adapter = esp32.start_bluetooth()
ble = BLERadio(adapter)
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    ble.start_advertising(advertisement)
    print("Waiting for the Bluefruit App to connect...")
    while not ble.connected:
        pass
    print("Bluefruit App is connected: waiting for UART input...")
    while ble.connected:
        # Returns b'' if nothing was read.
        one_byte = uart.read(1)
        if one_byte:
            print(one_byte)
            uart.write(one_byte)