# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate basic wifi communication with the Pico W.
# See https://learn.adafruit.com/pico-w-wifi-with-circuitpython for more details.
# Requires adafruit_requests.py in the lib/ folder
#
# No wiring is required.
import os
import ipaddress
import wifi

print("Connecting to WiFi")
wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
print("Connected to WiFi")
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
print("My IP address is", wifi.radio.ipv4_address)

ipv4 = ipaddress.ip_address("8.8.4.4")
print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))
