# DC motor Control w/ RPi motor driver board

import RPi.GPIO as GPIO


class control_motor:
    def __init__(self):
        # set GPIO pins
        self.pwm1 = 20
        self.pwm2 = 21
        self.D1 = 26

        GPIO.setup(self.pwm1, GPIO.OUT)
        GPIO.setup(self.pwm2, GPIO.OUT)
        GPIO.setup(self.D1, GPIO.OUT)
        self.p1 = GPIO.PWM(self.D1, 500)
        self.p1.start(75)

    def clockwise(self):
        GPIO.output(self.pwm1, 1)
        GPIO.output(self.pwm2, 0)

    def counterclockwise(self):
        GPIO.output(self.pwm1, 0)
        GPIO.output(self.pwm2, 1)
