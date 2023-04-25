import RPi.GPIO as GPIO
import time 

# set GPIO pins
pin_EN = 20
pin_1A = 21
pin_2A = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_EN, GPIO.OUT)
GPIO.setup(pin_1A, GPIO.OUT)
GPIO.setup(pin_2A, GPIO.OUT)

def clockwise():
    try:
        GPIO.output(pin_EN, True)
        GPIO.output(pin_2A, True)
    except Exception as e:
        print(e)

def counterclockwise():
    try:
        GPIO.output(pin_2A, True)
        GPIO.output(pin_1A, True)
    except Exception as e:
        print(e)
 
try:
    while True:
        counterclockwise()
#         time.sleep(6)
#         clockwise()
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()

