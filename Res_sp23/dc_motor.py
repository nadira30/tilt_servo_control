# DC motor Control w/ L293 H-Bridge ic
# Will Slaton
# December 17, 2019
# modified 4/26/2021

import RPi.GPIO as GPIO
import time

# set GPIO pins
pin_EN = 20 
pin_1A = 21 
pin_2A = 26 

run_time = 5# seconds

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_EN,GPIO.OUT)
GPIO.setup(pin_1A,GPIO.OUT)
GPIO.setup(pin_2A,GPIO.OUT)

class control_motor():
    
    def clockwise():
        try: 
            GPIO.output(pin_EN,True)
            GPIO.output(pin_2A,True)
        except Exception as e:
            print(e)
        
    def counterclockwise():
        try: 
            GPIO.output(pin_2A,True)
            GPIO.output(pin_1A,True)
        except Exception as e:
            print(e)    

try:
    start_time = time.time()
#     time.time() - start_time < run_time
    while time.time() - start_time < run_time :
        counterclockwise()
    while time.time() - start_time > run_time:
        clockwise()


except KeyboardInterrupt:
    print("That's all folks!")

finally:
    GPIO.cleanup()
    print("GPIO cleaned!")
