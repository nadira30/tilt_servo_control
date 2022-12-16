import RPi.GPIO as GPIO
import time
import decimal
import numpy as np
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory()
servo = AngularServo(20, min_angle =-180, max_angle=180, min_pulse_width= 0.0005, max_pulse_width= 0.0025, pin_factory=factory)
#set the tilt at the initial position vertical
servo.angle=100 # with ball at 0V

# mass of the ball i g
minitial= 228.3
mused= 65.28

#set pins
CS= 5                                                                      
CLK= 6
DO= 13
Din= 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(CS, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(DO, GPIO.IN)
GPIO.setup(Din, GPIO.OUT)
GPIO.setwarnings(False)
        
def readADC_channel(channel):
    
    #set initial binaruy string as empty
    d= ''
    #set the CS pin low
    GPIO.output(CS, False)
    #sleep for 0.01 ms
    time.sleep(0.0001)
    
    #set Din pin High
    GPIO.output(Din, True)
    
    #set the clock pin to low
    GPIO.output(CLK, False)
    #sleep
    time.sleep(0.0001)
    #set the clock pin to high
    GPIO.output(CLK, True)
    #sleep
    time.sleep(0.0001)
    #set the clock pin to low
    GPIO.output(CLK, False)
    #sleep
    time.sleep(0.0001)
    
     #channelvalidation
    if channel =='0' :
        din_control= '1000'
    elif channel =='1' :
        din_control= '1001'
    elif channel=='2':
        din_control= '1010'
    elif channel =='3':
        din_control= '1011'
    else:
        din_control='1100'
       
        
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
    
    #now read date synced to clock pulses
    for n in range (0,10):
        #set the clock pin to low
        GPIO.output(CLK, False)
        #sleep
        time.sleep(0.0001)
        #set the clock pin to high
        GPIO.output(CLK, True)
        #sleep
        time.sleep(0.0001)
        #set the clock pin to low
        GPIO.output(CLK, False)
        #sleep
        time.sleep(0.0001)
        # listen for the DO pin for a bit
        DO_state = GPIO.input(DO)
        if DO_state == True:
            d= d+ '1'
        else:
            d= d+'0'
    #set the CS pin high to end the conversation
    GPIO.output(CS, True)
    # Din low to reset the chip
    GPIO.output(Din, False)
    #return binary to user
    return d

#define a function to return the voltage
def calc_volts(d):
    # we know voltage is on 0 to 5V scale and
    # ADC0831 returns binary numbers w/ integer equivalent
    # values between 0 and 255
    d_int = int(d,2)
    # We ASSUME the voltage is exactly 5.0 volts out of the RPi
    # measure it to be sure and correct value below.
    volts = 5*d_int / 1024
    # but the step size is 5V / 256 steps = 0.01953... or about
    # 0.02 V V/step. Hence, we need to truncate our voltage value
    # to only display significant figures!
    volts = round(volts, 2)
    return volts

def resistance(volts):
    R = (volts*9940)/(5-volts)
    return R

try:
    start_time = time.time()
    vol=[]
    elapsed_time=0
    time_array = []
    my_Test= True
    
    while my_Test:
        elapsed_time = time.time()-start_time
        
        d0 = readADC_channel('1')
        # Convert the digital output of the IC into a voltage
        vol0= calc_volts(d0)
        vol.append(vol0)
        
        # control ball
        # angle varies from -180 to 180 degrees, clockwise = positive direction
        if vol0 < 2.4:
            servo.angle=(vol0*55/2.4)
            time.sleep(0.5)
        elif vol0 > 2.6:
            servo.angle = (vol0*55)/2.6
            time.sleep(0.5)
        else:
            print(f"Ball stationnary at v = {vol0}V where servo.angle = {servo.angle}")
            
        file = open('recorded_data/sensor_voltage2.txt', 'a')
        file.write(str(elapsed_time)+','+str(vol0)+ ',' +str(servo.angle)+ '\n')
        if elapsed_time >= 120:
            my_Test= False
            
        time.sleep(2)
    file.close()

except KeyboardInterrupt:
    print('Game over, Man!')
    GPIO.cleanup()
#     
finally:
    GPIO.cleanup()
