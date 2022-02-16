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
    from adafruit_bluefruit_connect.packet import Packet
    from adafruit_bluefruit_connect.color_packet import ColorPacket
    from adafruit_bluefruit_connect.button_packet import ButtonPacket
    from adafruit_bluefruit_connect.accelerometer_packet import AccelerometerPacket
    from adafruit_bluefruit_connect.gyro_packet import GyroPacket
    from adafruit_bluefruit_connect.location_packet import LocationPacket
    from adafruit_bluefruit_connect.magnetometer_packet import MagnetometerPacket
    from adafruit_bluefruit_connect.quaternion_packet import QuaternionPacket
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

# Set RAW=True to see the low-level bytes of data being transfered over BLE
# using either the UART or Controller modes of the Bluefruit App.
# Set RAW=False to try an interpret the different data packet formats sent
# by the Bluefruit App controller mode.
RAW = False

ButtonNames = ['', '1', '2', '3', '4', 'UP', 'DOWN', 'LEFT', 'RIGHT'];

while True:
    ble.start_advertising(advertisement)
    print("Waiting for the Bluefruit App to connect...")
    while not ble.connected:
        pass
    print("Bluefruit App is connected!")
    if RAW:
        print("waiting for UART input...")
    else:
        print("waiting for Controller input...")
    while ble.connected:
        if RAW:
            # Read a single byte. Returns b'' if nothing was read.
            one_byte = uart.read(1)
            if one_byte:
                # Print and echo the byte.
                print(one_byte)
                uart.write(one_byte)
        else:
            # Read controller packets.
            try:
                packet = Packet.from_stream(uart)
            except ValueError as e:
                print('Packet parse error:', e)
                continue
            if packet:
                name = packet.__class__.__name__
                if isinstance(packet, ColorPacket):
                    print('Color Packet:', packet.color)
                elif isinstance(packet, ButtonPacket):
                    button = ButtonNames[int(packet.button)]
                    state = 'pressed' if packet.pressed else 'released'
                    print(f'Button {button} {state}')
                elif isinstance(packet, (AccelerometerPacket, GyroPacket, MagnetometerPacket)):
                    print(f'{name}: x={packet.x:.3f} y={packet.y:.3f} z={packet.z:.3f}')
                elif isinstance(packet, LocationPacket):
                    print(f'Location: lat={packet.latitude:.3f} lon={packet.longitude:.3f} alt={packet.altitude:.3f}')
                else:
                    print(f'Received a new {name}')

    print('Disconnected')
