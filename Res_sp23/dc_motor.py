# DC motor Control w/ RPi motor driver board

import RPi.GPIO as GPIO
import time


class control_motor:
    def __init__(self):
        # set GPIO pins
        self.pin_EN = 20
        self.pin_1A = 21
        self.pin_2A = 26

        run_time = 5  # seconds

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_EN, GPIO.OUT)
        GPIO.setup(self.pin_1A, GPIO.OUT)
        GPIO.setup(self.pin_2A, GPIO.OUT)

    def clockwise(self):
        try:
            GPIO.output(self.pin_EN, True)
            GPIO.output(self.pin_2A, True)
        except Exception as e:
            print(e)

    def counterclockwise(self):
        try:
            GPIO.output(self.pin_2A, True)
            GPIO.output(self.pin_1A, True)
        except Exception as e:
            print(e)
