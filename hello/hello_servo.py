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
import time
import board
import pulseio

FREQUENCY = 50 # Hertz

PWM = pulseio.PWMOut(board.D2, frequency=FREQUENCY)

while True:
    for pulse_duration_ms in (0.7, 1.4, 1.5, 1.6, 2.3):
        print(pulse_duration_ms)
        PWM.duty_cycle = int(0xffff * (pulse_duration_ms / 1000 * FREQUENCY))
        time.sleep(2)
