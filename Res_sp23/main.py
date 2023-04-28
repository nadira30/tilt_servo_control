# main script
import RPi.GPIO as GPIO
import time

from adc_calculation import readADC_channel, calc_volts
from dc_motor import control_motor
import numpy as np

# mass of the ball i g
m = 228.3


K_PL = 40
K_PR = 38

try:
    my_Test = True
    motor = control_motor()

    while my_Test:

        d0 = readADC_channel('1')
        # Convert the digital output of the IC into a voltage
        vol0 = calc_volts(d0)
        print(vol0)

        #         p1.ChangeDutyCycle(vol0*75/5)
        # c*delta
        delta = vol0 - 2.5

        if delta < 0:
            duty_cycle = np.abs(delta) * K_PR
            motor.p1.ChangeDutyCycle(duty_cycle)
            motor.counterclockwise()

        elif delta > 0:
            duty_cycle = np.abs(delta) * K_PL
            motor.p1.ChangeDutyCycle(duty_cycle)
            motor.clockwise()
        else:
            print("ball at the middle")
            time.sleep(0.0001)

except KeyboardInterrupt:
    print('Game over, Man!')
    GPIO.cleanup()

finally:
    GPIO.cleanup()
