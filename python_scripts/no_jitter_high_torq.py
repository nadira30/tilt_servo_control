from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory()
servo = AngularServo(20, min_angle =-180, max_angle=180, min_pulse_width= 0.0005, max_pulse_width= 0.0025, pin_factory=factory)
# initial position
servo.angle = 0
# # 
# while (True):
#     servo.angle = -90
#     sleep(3)
#     servo.angle = 0
#     sleep(2)
#     servo.angle = 180
#     sleep(3)
    #servo.angle = 90
    #sleep(2)
    #         

