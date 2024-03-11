# Wireless Communication

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

## Introduction

The W in "Pico W" stands for wireless.  Wireless communication uses microwave frequencies near 2.4GHz and 5.0GHz that are shared with Bluetooth and other communications protocols (since it is unregulated) as well as microwave ovens!  All that sharing leads to a rather complex protocol that requires its own dedicated processor, as well as specialized circuitry capable of handling very high frequency signals.  You can usually identify a microwave radio interface on a circuit board because it is enclosed in a metal shield to minimize [electromagnetic inteference](https://en.wikipedia.org/wiki/Electromagnetic_interference) with other devices, as required for consumer product certification. There should also be an antenna visible, or a connector for an external antenna. The size of an antenna is generally matched to the wavelengths of interest, which are in the centimeter-range for microwaves.

Identify the radio interface and antenna on your Pico W module.

## Connecting to the Campus Wifi Network

These instructions are specific to the UC Irvine campus.

The first step is to look up the unique serial number that identifies the wifi interface in your Pico-W, by running this program:
```python
import wifi

print('This Pico has MAC address', ''.join([f'{x:02x}' for x in wifi.radio.mac_address]))
```
Once you have this address, add it to this [google doc](https://docs.google.com/document/d/1SInJS43dUKPVPPTKneOm0zg-gH_mzby6MhSexpALxpM/edit?usp=sharing) so the instructor can temporarily grant access to the campus wifi. In case you want to do this yourself outside of class, start [here](https://mobileaccess.oit.uci.edu/registration/).

A [MAC address](https://en.wikipedia.org/wiki/MAC_address) is a permanent identifier associated with your wifi interface.
It is assigned at the factory and identifies the manufacturer. Try entering the address for your device [here](https://maclookup.app/search) to confirm this.

This program uses the [wifi library](https://docs.circuitpython.org/en/latest/shared-bindings/wifi/index.html) to establish communications between the Pico wifi interface and microcontroller.

Next, verify that you can connect to the campus network using this program:
```python
import ipaddress
import wifi

print('Connecting to WiFi...')
wifi.radio.connect('UCInet Mobile Access')
print('Connected to WiFi')

# Lookup our temporarily assigned (IP) address.
print('My IP address is', wifi.radio.ipv4_address)

# Try to "ping" the google servers.
ipv4 = ipaddress.ip_address('8.8.4.4')
print('Ping google.com: %f ms' % (wifi.radio.ping(ipv4)*1000))
```

Note that the campus network is unusual since it requires pre-registration of a MAC address but then no password when you connect. If you wanted to connect to a more typical network instead, you would use:
```python
wifi.radio.connect(ESSID, pw)
```
where `ESSID` is the [network name](https://en.wikipedia.org/wiki/Service_set_(802.11_network)#SSID) and `pw` is the network password. Since the password is in plain text in your code, be careful not to publish this code anywhere publicly visible (such as github).

This program prints an [IP address](https://en.wikipedia.org/wiki/IP_address), which is a temporary identifier assigned when you join the network (using the DHCP protocol). The IP address is how your identify yourself to other computers over the internet. Within the UCI campus network, all IP addresses have the same initial numbers.

The last two lines of the program perform a simple test that your Pico can send and receive data using the [Ping protocol](https://en.wikipedia.org/wiki/Ping_(networking_utility)).  This test attempts to send a small packet of data to a google server then times how long the response takes. Notice how this is quite similar to a [sonar distance measurement](sonar.md)!

Typical output from this program would be:
```
Connecting to WiFi...
Connected to WiFi
My IP address is 169.234.42.56
Ping google.com: 75.999969 ms
```

## Log Data to a Google Spreadsheet

Here is a more complex example of using the [requests library](https://docs.circuitpython.org/projects/requests/en/latest/api.html) to access cloud-based services via their web-based APIs, i.e. by accessing specially prepared URLs via the HTTP protocol. In this case, we are logging data to a google spreadsheet using the google form API:
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
wifi.radio.connect('UCInet Mobile Access')
print('Connected to WiFi')

# Lookup our permanent (MAC) and temporarily assigned (IP) addresses.
# https://en.wikipedia.org/wiki/MAC_address
MACaddr = ''.join([f'{i:02x}' for i in wifi.radio.mac_address])
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

The example above uses a shared form but can you also create your own form for data logging. Here are the instructions to recreate a form similar to the one used above:
 1. Visit https://docs.google.com/forms/ and create a blank form
 2. Create four questions, named "version", "MACaddr", "IPaddr" and "data". You can change these names but it will be easier to fill the form via python if you use names that are valid python identifiers (i.e. avoid spaces and punctuation).
 3. Verify that the first 3 questions have the "Short Answer" type and the last one (for "data") has the "Paragraph" type.
 4. Use the "Get pre-filled link" menu item and set the answers equal to the question name for all 4 questions.
 5. Copy the link into the code above at this line:
 ```python
 PREFILLED=`...prefilled link goes here...`
 ```

You can change the number and names of each question to suit your application, but make sure that this line matches your choices:
```python
    submit(version=1, MACaddr=MACaddr, IPaddr=IPaddr, data=data)
```
