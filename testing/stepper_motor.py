#!/usr/bin/python

# Author: Dave Young
# Created: 8-20-2017


### Imports ###
import RPi.GPIO as GPIO
import time


### Constants and Setups ###
delay=3
steps = 512

enable_pin = 18
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24

GPIO.setmode(GPIO.BCM)

GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

GPIO.output(enable_pin, 1)


### Functions ###
def forward(delay, steps):
  for i in range(0, steps):
    setStep(1, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)
  print("forward")

def backwards(delay, steps):
  for i in range(0, steps):
    setStep(1, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(1, 0, 1, 0)
    time.sleep(delay)


def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)


### Test Runs ###
try:
        
    while True:
      forward(int(delay) / 1000.0, int(steps))
#   steps = raw_input("How many steps backwards? ")
      backwards(int(delay) / 1000.0, int(steps))


# my quick take on it for tests
# forward(int(delay) / 1000.0, int(steps))
#backwards(int(delay) / 1000.0, int(steps))

# found the motor was holding and heating up after program was stopped.
#   put this in to fix that.
except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()
