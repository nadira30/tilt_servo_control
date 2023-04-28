import time
from adafruit_crickit import crickit

motor = crickit.dc_motor_1

motor.throttle=0.5

while True:
    time.sleep(1)