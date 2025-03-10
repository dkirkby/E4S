# Wireless Communication

*Material for a [UC Irvine](https://uci.edu/) course offered by the [Department of Physics Astronomy](https://www.physics.uci.edu/) and developed by [David Kirkby](https://faculty.sites.uci.edu/dkirkby/).*

## Introduction

The W in "Pico W" stands for wireless.  Wireless communication uses microwave frequencies near 2.4GHz and 5.0GHz that are shared with Bluetooth and other communications protocols (since it is unregulated) as well as microwave ovens!  All that sharing leads to a rather complex protocol that requires its own dedicated processor, as well as specialized circuitry capable of handling very high frequency signals.  You can usually identify a microwave radio interface on a circuit board because it is enclosed in a metal shield to minimize [electromagnetic inteference](https://en.wikipedia.org/wiki/Electromagnetic_interference) with other devices, as required for consumer product certification. There should also be an antenna visible, or a connector for an external antenna. The size of an antenna is generally matched to the wavelengths of interest, which are in the centimeter-range for microwaves.

Identify the [radio interface](https://www.infineon.com/cms/en/product/wireless-connectivity/airoc-wi-fi-plus-bluetooth-combos/wi-fi-4-802.11n/cyw43439/) and [antenna](https://abracon.com/niche-antennas) on your Pico W module:

![Pico W PCB](img/pico-w-pcb.jpg)

> The programs below will sometimes fail with mysterious errors, but should eventually succeed if you keep retrying.

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
import time
import ipaddress
import wifi

print('Connecting to WiFi...')
wifi.radio.connect(ssid='UCInet Mobile Access')
print('Connected to WiFi')

# Lookup our temporarily assigned (IP) address.
print('My IP address is', wifi.radio.ipv4_address)

# Try to "ping" the google servers.
ping_ip = ipaddress.IPv4Address("8.8.8.8")  # Google.com
ntry = 10
for i in range(ntry):
    ping = wifi.radio.ping(ip=ping_ip)
    print(f'ping {i+1}/{ntry}: {ping}')
    time.sleep(1)
```

Note that the campus network is unusual since it requires pre-registration of a MAC address but then no password when you connect. If you wanted to connect to a more typical network instead, you would use:
```python
wifi.radio.connect(ssid=ESSID, password=pw)
```
where `ESSID` is the [network name](https://en.wikipedia.org/wiki/Service_set_(802.11_network)#SSID) and `pw` is the network password. Since the password is in plain text in your code, be careful not to publish this code anywhere publicly visible (such as github).

This program prints an [IP address](https://en.wikipedia.org/wiki/IP_address), which is a temporary identifier assigned when you join the network (using the DHCP protocol). The IP address is how your identify yourself to other computers over the internet. Within the UCI campus network, all IP addresses have the same initial numbers.

The final lines of the program perform a simple test that your Pico can send and receive data using the [Ping protocol](https://en.wikipedia.org/wiki/Ping_(networking_utility)).  This test attempts to send a small packet of data to a google server then times how long the response takes. Notice how this is quite similar to a [sonar distance measurement](sonar.md)! Initial ping attempts often fail, but you should eventually see numerical values which are the round-trip packet time in seconds.

Typical output from this program would be:
```
Connecting to WiFi...
Connected to WiFi
My IP address is 192.168.87.27
ping 1/10: None
ping 2/10: None
ping 3/10: None
ping 4/10: 0.056
ping 5/10: 0.02
ping 6/10: 0.02
ping 7/10: 0.019
ping 8/10: 0.034
ping 9/10: 0.023
ping 10/10: 0.014
```

## Read a Web Page

Next, we will use the [adafruit requests library](https://docs.circuitpython.org/projects/requests/en/latest/api.html)
to access a web page. This library is a stripped-down version of the widely used
[python requests package](https://requests.readthedocs.io/en/latest/). Note that when we access a web
page using code, we are downloading its data using the HTTP protocol, but will not see it rendered the way
you are used to in a web browser. Therefore, it is helpful to test using some simple web pages where the
data we download is easy to interpret. For example, try these in your browser:
 - http://wifitest.adafruit.com/testwifi/index.html
 - https://wttr.in/Irvine
 - https://uci.edu/

To see how these pages will appear to a program, use the "View Source" menu option in your browser.

Here is a program to read a web page and print its contents:
```python
import wifi
import adafruit_connection_manager
import adafruit_requests

print('Connecting to WiFi...')
wifi.radio.connect(ssid='UCInet Mobile Access')
print('Connected to WiFi')

# Lookup our temporarily assigned (IP) address.
print('My IP address is', wifi.radio.ipv4_address)

# Initialize HTTP access
print('Initializing requests library...')
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
print('Success!')

with requests.get("http://wifitest.adafruit.com/testwifi/index.html") as response:
    print(response.text)
```

> If you get an error in the Mu Editor Serial port about missing `adafruit_connection_manager`, download it from [here](bin/adafruit_connection_manager.mpy?raw=true) and copy into the `lib` folder on your `CIRCUITPY` USB drive.

## Log Data to a Google Spreadsheet

Here is a more complex example of using the [requests library](https://docs.circuitpython.org/projects/requests/en/latest/api.html)
to access cloud-based services via their web-based APIs, i.e. by accessing specially prepared URLs via the HTTP protocol. In this case, we are logging data to a google spreadsheet using the google form API:
```python
import time
import json
import ipaddress
import wifi
import adafruit_connection_manager
import adafruit_requests
import adafruit_dps310

# Initialize pressure sensor
print('Initializing pressure sensor...')
sda, scl = board.GP0, board.GP1
i2c = busio.I2C(sda=sda, scl=scl)
tpsensor = adafruit_dps310.DPS310(i2c)

print('Connecting to WiFi...')
wifi.radio.connect(ssid='UCInet Mobile Access')
print('Connected to WiFi')

# Initialize the requests library for use with our wifi connection.
# See https://docs.circuitpython.org/projects/requests/en/latest/api.html
print('Initializing requests library...')
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)
print('Success!')

# Get the prefilled URL for a google form that does not require any sign in or authentication.
# The values you type into the prefilled form are the placeholders used to identify each value
# passed to the submit() function defined below.
PREFILLED='https://docs.google.com/forms/d/e/1FAIpQLSddxA63cvCGBxfKTqH3aemRZ4BPDJ6PCZpEdmSa9DpFsNQ1Nw/viewform?usp=pp_url&entry.1607031342=TEMPERATURE&entry.2073013553=PRESSURE'

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

for i in range(5):
    temperature = tpsensor.temperature
    pressure = tpsensor.pressure
    submit(TEMPERATURE=temperature, PRESSURE=pressure)
    time.sleep(1)
```
Typical output from this program would be:
```
Initializing pressure sensor...
Connecting to WiFi...
Connected to WiFi
Initializing requests library...
Success!
Read T=22.10C P=1011.45hPa
Read T=22.10C P=1011.46hPa
Read T=22.10C P=1011.45hPa
Read T=22.10C P=1011.46hPa
Read T=22.10C P=1011.45hPa
```
If you see these lines, you should also see corresponding new rows in the spreadsheet that automatically records all of the google form submissions. Note that each row is automatically assigned a timestamp, so you have a record of when the data was sent.

This template can be modified to automatically log any type of sensor data to the cloud that is recorded by your circuit, assuming that you have access to a wifi network.

The example above uses a shared form but can you also create your own form for data logging. Here are the instructions to recreate a form similar to the one used above:
 1. Visit https://docs.google.com/forms/ and create a blank form
 2. Create four questions, named "version", "MACaddr", "IPaddr" and "data". You can change these names but it will be easier to fill the form via python if you use names that are valid python identifiers (i.e. avoid spaces and punctuation).
 3. Verify that the first 3 questions have the "Short Answer" type and the last one (for "data") has the "Paragraph" type.
 4. Publish your form and set the "Responder view" to "Anyone with the link".
 5. Use the "Get pre-filled link" menu item and set the answers equal to the question name for all 4 questions.
 6. Copy the link into the code above at this line:
 ```python
 PREFILLED=`...prefilled link goes here...`
 ```

You can change the number and names of each question to suit your application, but make sure that this line matches your choices:
```python
    submit(TEMPERATURE=temperature, PRESSURE=pressure)
```

## Serve a Web Page

As a final example, we show how the Pico W can run a lightweight web server that you can connect to from a browser running on a different device (laptop, phone, etc). This simple code just displays a static web page, but could be expanded to display some buttons that control your circuit, for example. The design technique of replacing physical switches, knobs, sliders, etc, with their web (or native app) equivalents leads to lower costs and greater flexibility (since changes can be made even after the circuit is built). Many designs today adopt this approach, but the downside for users is that even basic operation now requires a wifi connection and app.

Here is the simple code for getting started. See [here](https://docs.circuitpython.org/projects/httpserver/en/stable/index.html) for more details and advanced documentation.
```python
import wifi
import microcontroller
import adafruit_connection_manager
import adafruit_httpserver

print('Connecting to WiFi...')
wifi.radio.connect(ssid='UCInet Mobile Access')
print('Connected to WiFi at', wifi.radio.ipv4_address)

# Initialize the web server
print('Initializing web server...')
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
server = adafruit_httpserver.Server(pool, "/static", debug=True)

# Define the default web page to serve
content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <title>Pico W HTTP Server</title>
</body>
"""

@server.route("/")
def base(request: adafruit_httpserver.Request):
    return adafruit_httpserver.Response(request, content, content_type='text/html')

server.serve_forever(str(wifi.radio.ipv4_address))
```

> Since this site uses HTTP (instead of HTTPS) many browsers (including chrome and firefox) will not load it by default.
