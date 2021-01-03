# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Display 3 lines of text on the 128 x 32 OLED display
# connected via the built-in I2C interface.
import time

import board
import displayio
import terminalio

# Copy these into your lib/ folder
from adafruit_display_text import label
import adafruit_displayio_ssd1306

displayio.release_displays()

i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)

WIDTH = 128
HEIGHT = 32

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

DISPLAY_LINES = 3
LINE_HEIGHT = 12
MAX_DISPLAY_CHARS = 21

splash = displayio.Group(max_size=DISPLAY_LINES)
display.show(splash)
display_lines = []

for i in range(DISPLAY_LINES):
    display_lines.append(
        label.Label(terminalio.FONT, text='', color=0xffffff, x=0,
        y=LINE_HEIGHT * i + 3, max_glyphs=MAX_DISPLAY_CHARS))
    splash.append(display_lines[-1])

ALIGN_LEFT = 0
ALIGN_RIGHT = 1
ALIGN_CENTER = 2

def display_text(line, text, align=ALIGN_LEFT):
    trimmed = text[:MAX_DISPLAY_CHARS]
    if align == ALIGN_RIGHT:
        npad = MAX_DISPLAY_CHARS - len(trimmed)
    elif align == ALIGN_CENTER:
        npad = (MAX_DISPLAY_CHARS - len(trimmed)) // 2
    else:
        npad = 0
    display_lines[line % DISPLAY_LINES].text = (' ' * npad) + trimmed

display_text(0, 'UCI Electronics', ALIGN_LEFT)
display_text(1, 'for Scientists', ALIGN_CENTER)
display_text(2, 'P120/220', ALIGN_RIGHT)

while True:
    time.sleep(1)
