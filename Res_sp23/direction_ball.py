import RPi.GPIO as GPIO
import time
from time import sleep
from dc_motor import control_motor
import numpy as np
# mass of the ball i g
m = 228.3

# set pins
CS = 5
CLK = 6
DO = 13
Din = 16

K_PL=40
K_PR=30


GPIO.setmode(GPIO.BCM)

GPIO.setup(CS, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DO, GPIO.IN)
GPIO.setup(Din, GPIO.OUT)
# set GPIO pins
pwm1 = 20
pwm2 = 21
D1 = 26

GPIO.setup(pwm1, GPIO.OUT)
GPIO.setup(pwm2, GPIO.OUT)
GPIO.setup(D1, GPIO.OUT)
p1=GPIO.PWM(D1,500)
p1.start(75)

def set_motor(A1,A2):
    GPIO.output(pwm1,A1)
    GPIO.output(pwm2,A2)

def clockwise():
    GPIO.output(pwm1, 1)
    GPIO.output(pwm2, 0)

def counterclockwise():
    GPIO.output(pwm1, 0)
    GPIO.output(pwm2, 1)


def readADC_channel(channel):
    # set initial binaruy string as empty
    d = ''
    # set the CS pin low
    GPIO.output(CS, False)
    # sleep for 0.01 ms
    time.sleep(0.0001)

    # set Din pin High
    GPIO.output(Din, True)

    # set the clock pin to low
    GPIO.output(CLK, False)
    # sleep
    time.sleep(0.0001)
    # set the clock pin to high
    GPIO.output(CLK, True)
    # sleep
    time.sleep(0.0001)
    # set the clock pin to low
    GPIO.output(CLK, False)
    # sleep
    time.sleep(0.0001)

    # channelvalidation
    if channel == '0':
        din_control = '1000'
    elif channel == '1':
        din_control = '1001'
    elif channel == '2':
        din_control = '1010'
    elif channel == '3':
        din_control = '1011'
    else:
        din_control = '1100'

    # send din_control to Din pin
    for n in din_control:
        if n == '0':
            GPIO.output(Din, False)
        else:
            GPIO.output(Din, True)

        GPIO.output(CLK, False)
        GPIO.output(CLK, True)
        GPIO.output(CLK, False)

    GPIO.output(CLK, False)
    GPIO.output(CLK, True)
    GPIO.output(CLK, False)

    # now read date synced to clock pulses
    for n in range(0, 10):
        # set the clock pin to low
        GPIO.output(CLK, False)
        # sleep
        time.sleep(0.0001)
        # set the clock pin to high
        GPIO.output(CLK, True)
        # sleep
        time.sleep(0.0001)
        # set the clock pin to low
        GPIO.output(CLK, False)
        # sleep
        time.sleep(0.0001)
        # listen for the DO pin for a bit
        DO_state = GPIO.input(DO)
        if DO_state == True:
            d = d + '1'
        else:
            d = d + '0'
    # set the CS pin high to end the conversation
    GPIO.output(CS, True)
    # Din low to reset the chip
    GPIO.output(Din, False)
    # return binary to user
    return d


# define a function to return the voltage
def calc_volts(d):
    # we know voltage is on 0 to 5V scale and
    # ADC0831 returns binary numbers w/ integer equivalent
    # values between 0 and 255
    d_int = int(d, 2)
    # We ASSUME the voltage is exactly 5.0 volts out of the RPi
    # measure it to be sure and correct value below.
    volts = 5 * d_int / 1024
    # but the step size is 5V / 256 steps = 0.01953... or about
    # 0.02 V V/step. Hence, we need to truncate our voltage value
    # to only display significant figures!
    volts = round(volts, 2)
    return volts


def resistance(volts):
    R = (volts * 9940) / (5 - volts)
    return R


try:
    start_time = time.time()
    vol = []
    previous = 0
    current = 0
    my_Test = True

    while my_Test:

        d0 = readADC_channel('1')
        # Convert the digital output of the IC into a voltage
        vol0 = calc_volts(d0)
        print(vol0)
        
#         p1.ChangeDutyCycle(vol0*75/5)
# c*delta
        delta= vol0-2.5
        
        if delta<0:
            duty_cycle=np.abs(delta)*K_PR
            p1.ChangeDutyCycle(duty_cycle)
            counterclockwise()
            
        elif delta>0:
            duty_cycle=np.abs(delta)*K_PL
            p1.ChangeDutyCycle(duty_cycle)
            clockwise()
#             print( "bal rolling to the right")
        else:
            print("ball at the middle")
            time.sleep(0.001)           
        


except KeyboardInterrupt:
    print('Game over, Man!')
    GPIO.cleanup()
#     
finally:
    GPIO.cleanup()
