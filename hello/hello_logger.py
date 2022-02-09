# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate data logging over wifi with
# the Metro M4 airlift's on-board ESP32.
#
# The libraries needed to communicate with the ESP32 in this
# example should already be included with the M4 Airlift
# CircuitPython installation.
#
# The URL we write to below submits a google form.
#
# No wiring is required.
import time
import json

import board
import digitalio

try:
    # These libraries should be installed in the M4 airlib lib/ folder
    import adafruit_esp32spi.adafruit_esp32spi_socket as socket
    import adafruit_esp32spi.adafruit_esp32spi
    import adafruit_requests as requests
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
do_connect = True

# Get our firmware version and wireless ethernet MAC address.
version = str(esp.firmware_version, 'ascii')
MACaddr = '.'.join([f'{i:02x}' for i in esp.MAC_address])
print(f'Firmware {version} MAC address {MACaddr}')

# Try to connect to the wifi network specified in secrets.py
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
        print(f'Connection failed (will retry): {e}')
        time.sleep(1)
IPaddr = esp.pretty_ip(esp.ip_address)
print(f'Connected as {IPaddr}')

requests.set_socket(socket, esp)

# Get the prefilled URL for a google form that does not require any sign in or authentication.
# The values you type into the prefilled form are the placeholders used to identify each value
# passed to the submit() function defined below.
PREFILLED='https://docs.google.com/forms/d/e/1FAIpQLSdck4ybXdYOxhM2syRVQpQcQ8GBuTcWGCFtdxDDxNZ7QivJmw/viewform?usp=pp_url&entry.744442955=version&entry.954313297=MACaddr&entry.678802473=IPaddr&entry.824900847=data'

POST_URL = PREFILLED[:PREFILLED.index('viewform?')] + 'formResponse'

FIELDS = {}
for token in PREFILLED.split('&entry.')[1:]:
    idnum, placeholder = token.split('=')
    FIELDS[placeholder] = 'entry.' + idnum

def submit(**kwargs):
    data = {}
    for placeholder, value in kwargs.items():
        if placeholder not in FIELDS:
            print(f'Ignoring unexpected placeholder {placeholder}')
        else:
            data[FIELDS[placeholder]] = value
    r = requests.post(POST_URL, data=data)
    if r.status_code != 200:
        print(f'Error submitting data: {r.status_code}')

for i in range(3):
    data = json.dumps({"i":i})
    print(f'sending data: {data}')
    submit(version=version, MACaddr=MACaddr, IPaddr=IPaddr, data=data)
    time.sleep(1)
