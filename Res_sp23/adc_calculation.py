import RPi.GPIO as GPIO
import time

# set pins
CS = 5
CLK = 6
DO = 13
Din = 16

GPIO.setup(CS, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DO, GPIO.IN)
GPIO.setup(Din, GPIO.OUT)

GPIO.setmode(GPIO.BCM)


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
