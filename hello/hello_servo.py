# UCI Electronics for Scientists
# https://github.com/dkirkby/E4S
#
# Demonstrate control of the continuous server motor
# using PWM signals directly.
# Connections are:
# M4 GND - servo brown
# M4 3.3V - servo red
# M4 D2 - servo orange
# Optional: connect the 470uF capacitor between 3.3V and GND
#
# For the Pi Pico, use GP00-28 instead of D2.
import time
import board
import pwmio

FREQUENCY = 50 # Hertz
PERIOD_MS = 1000 / FREQUENCY

PWM = pwmio.PWMOut(board.GP22, frequency=FREQUENCY)

while True:
    for pulse_duration_ms in (0.7, 1.4, 1.5, 1.6, 2.3):
        PWM.duty_cycle = int(0xffff * (pulse_duration_ms / PERIOD_MS))
        print(f'pulse duration={pulse_duration_ms:.1f}ms, PWM.duty_cyle=0x{PWM.duty_cycle:04x}')
        time.sleep(2)
