from gpiozero import Robot, PhaseEnableRobot, Motor
import RPi.GPIO as GPIO
import time

motor = Motor(26,20,21)
# motor.forward(speed=1)
# time.sleep(6)
# motor.stop()
# time.sleep(4)
# motor.reverse()
# motor.backward(speed=1)
# time.sleep(10)
# motor.stop()
# GPIO.cleanup()
offset = 10
status=True
start_time= time.time()
while(status):
    time_elapsed= time.time()-start_time
#     motor.backward()
#     time.sleep(2)
    motor.forward()
    time.sleep(4)
    motor.backward()
    if time_elapsed>=offset:
        status=False
motor.stop()
GPIO.cleanup()
    
    
