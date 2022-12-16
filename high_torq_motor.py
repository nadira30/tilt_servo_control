from gpiozero import AngularServo, Servo
from time import sleep

servo = AngularServo(20, min_angle =0, max_angle=270, min_pulse_width= 0.0005, max_pulse_width= 0.0025)

while (True):
    servo.angle = 0
    sleep(5)
    servo.angle = 10
    sleep(6)


