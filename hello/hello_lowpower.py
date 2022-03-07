# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate low-power programming techniques.
# The M4 does not support the PinAlarm feature used here, so
# this example only runs on the Pi Pico.
#
# See https://learn.adafruit.com/deep-sleep-with-circuitpython
# for more details.
import time

import board
import digitalio
import alarm

# Why did we wake up?
wake_trigger = alarm.wake_alarm
if wake_trigger is None:
    # This is the initial boot, before any deep sleep.
    nblink = 5
elif isinstance(wake_trigger, alarm.time.TimeAlarm):
    nblink = 1
elif isinstance(wake_trigger, alarm.pin.PinAlarm):
    nblink = 2

# Use the onboard LED to signal why we woke up.
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
blink_time = 0.1 # seconds
for i in range(nblink):
    led.value = True
    time.sleep(blink_time)
    led.value = False
    time.sleep(blink_time)

# Return to deep sleep mode, waiting for the next wake trigger.
alarm_duration = 5 # seconds
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + alarm_duration)
switch_alarm = alarm.pin.PinAlarm(pin=board.GP2, value=False, pull=True)
alarm.exit_and_deep_sleep_until_alarms(time_alarm, switch_alarm)
