# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate basic wifi communication with
# the Metro M4 airlift's on-board ESP32.
#
# The libraries needed to communicate with the ESP32 in this
# example should already be included with the M4 Airlift
# CircuitPython installation.
#
# For more advanced examples (which need additional libraries), see
# https://github.com/adafruit/Adafruit_CircuitPython_ESP32SPI/tree/master/examples
#
# No wiring is required.
import time

import board
import digitalio

try:
    # These libraries should be included in the M4 airlift
    # CircuitPython installation.
    import adafruit_esp32spi.adafruit_esp32spi_socket
    import adafruit_esp32spi.adafruit_esp32spi
except ImportError as e:
    print(e)
    print('Are you running on an M4 Airlift?')
    while True: pass

# Define the digital lines that interface with the ESP32 chip.
esp32_cs = digitalio.DigitalInOut(board.ESP_CS)
esp32_ready = digitalio.DigitalInOut(board.ESP_BUSY)
esp32_reset = digitalio.DigitalInOut(board.ESP_RESET)

# Initialize the M4 hardware SPI bus.
spi = board.SPI()

# Initialize ESP32 control via SPI.
esp = adafruit_esp32spi.adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# Specify running options.
do_scan = False
do_connect = False

# Get our firmware version and wireless ethernet MAC address.
version = str(esp.firmware_version, 'ascii')
macaddr = '.'.join([f'{i:02x}' for i in esp.MAC_address])
print(f'ESP32 firmware version: {version}')
print(f'ESP32 wifi MAC address: {macaddr}')

# Check that the ESP32 is idle.
if esp.status == adafruit_esp32spi.adafruit_esp32spi.WL_IDLE_STATUS:
    print('ESP32 is in idle mode')

# Scan for wifi networks.
if do_scan:
    print('Scanning for wifi networks...')
    for access_point in esp.scan_networks():
        ssid = str(access_point['ssid'], 'utf-8')
        rssi = access_point['rssi']
        # https://www.metageek.com/training/resources/understanding-rssi.html
        print(f'Found "{ssid}" with signal strength {rssi}dB.')

# Try to connect to a network.
if do_connect:
    try:
        from secrets import secrets
        ssid, password = secrets['ssid'], secrets['password']
    except ImportError as e:
        print('Save a file called secrets.py on your M4 containing:')
        print('secrets = dict(ssid="network_name", password="mypw")')
        while True: pass
    print(f'Trying to connect to "{ssid}"...')
    while not esp.is_connected:
        try:
            esp.connect_AP(ssid, password)
        except RuntimeError as e:
            print(f'Connection failed: {e}')
    print('Connected!')
    # Do periodic pings and print the results.
    HOST = 'google.com'
    print(f'Pinging {HOST}...')
    while True:
        delay = esp.ping(HOST)
        print(f'delay {delay}ms')
        time.sleep(1)
