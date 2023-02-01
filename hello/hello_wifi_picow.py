# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate basic wifi communication with the Pico W.
# See https://learn.adafruit.com/pico-w-wifi-with-circuitpython for more details.
# Requires adafruit_requests.py in the lib/ folder
#
# No wiring is required.
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
ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))
