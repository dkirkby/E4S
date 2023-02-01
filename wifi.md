# Wireless Communication

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

## Introduction

The W in "Pico W" stands for wireless.  Wireless communication uses microwave frequencies near 2.4GHz and 5.0GHz that are shared with Bluetooth and other communications protocols (since it is unregulated) as well as microwave ovens!  All that sharing leads to a rather complex protocol that requires its own dedicated processor, as well as specialized circuitry capable of handling very high frequency signals.  You can usually identify a microwave radio interface on a circuit board because it is enclosed in a metal shield to minimize [electromagnetic inteference](https://en.wikipedia.org/wiki/Electromagnetic_interference) with other devices, as required for consumer product certification. There should also be an antenna visible, or a connector for an external antenna. The size of an antenna is generally matched to the wavelengths of interest, which are in the centimeter-range for microwaves.

Identify the radio interface and antenna on your Pico W module.

## Establishing and Testing a WiFi Connection

Connect a Pico W to your laptop via USB.  You do not need any external components to establish a wifi connection.  Test your connection using this program:
```python
import ipaddress
import wifi

print('Connecting to WiFi...')
# The arguments are the network SSID and password.
# These values are for a temporary network in the classroom.
wifi.radio.connect('E4Sclassroom', 'anteater')
print('Connected to WiFi')

# Lookup our permanent (MAC) and temporarily assigned (IP) addresses.
# https://en.wikipedia.org/wiki/MAC_address
print('My MAC address is', '-'.join([f'{i:02x}' for i in wifi.radio.mac_address]))
print('My IP address is', wifi.radio.ipv4_address)

# Try to "ping" the google servers.
ipv4 = ipaddress.ip_address('8.8.4.4')
print('Ping google.com: %f ms' % (wifi.radio.ping(ipv4)*1000))
```

Note that we are using a temporary WiFi network in the classroom instead of connecting directly to the campus wifi network, in order to simplify the authentication process.  The temporary network name (aka ESSID) and password appear in the `wifi.radio.connect` line above.

Once you have connected to this temporary network, the program prints two addresses associated with the connection:
 - the [MAC address](https://en.wikipedia.org/wiki/MAC_address) is a permanent identifier associated with your wifi connection device.
 - the [IP address](https://en.wikipedia.org/wiki/IP_address) is a temporary identifier assigned when you join the network (using the DHCP protocol).

The MAC address is assigned at the factory and the initial values identify the manufacturer. Try entering the address for your device [here](https://maclookup.app/search) to confirm this.

The IP address is how your identify yourself to other computers over the internet. Within the UCI campus network, all IP addresses have the same initial numbers.

The last two lines of the program perform a simple test that your Pico can send and receive data using the [Ping protocol](https://en.wikipedia.org/wiki/Ping_(networking_utility)).  This test attempts to send a small packet of data to a google server then times how long the response takes. Notice how this is quite similar to a [sonar distance measurement](sonar.md)!

## Log Data to a Google Spreadsheet

Here is a more complex example of using the [requests library]() to access cloud-based services via their web-based APIs, i.e. by accessing specially prepared URLs via the HTTP protocol. In this case,
we are logging data to a google spreadsheet using the google form API:
```python
import time
import json
import ipaddress
import wifi
import ssl
import socketpool
import adafruit_requests

print('Connecting to WiFi...')
# The arguments are the network SSID and password.
# These values are for a temporary network in the classroom.
wifi.radio.connect('E4Sclassroom', 'anteater')
print('Connected to WiFi')

# Lookup our permanent (MAC) and temporarily assigned (IP) addresses.
# https://en.wikipedia.org/wiki/MAC_address
MACaddr = '-'.join([f'{i:02x}' for i in wifi.radio.mac_address])
print('My MAC address is', MACaddr)
IPaddr = wifi.radio.ipv4_address
print('My IP address is', IPaddr)

# Initialize the requests library for use with our wifi connection.
# See https://docs.circuitpython.org/projects/requests/en/latest/api.html
print('Initializing requests library...')
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())
print('Success!')

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
    submit(version=1, MACaddr=MACaddr, IPaddr=IPaddr, data=data)
    time.sleep(1)
```
