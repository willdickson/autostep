from __future__ import print_function
from autostep import Autostep
import time

port = '/dev/ttyACM0'

stepper = Autostep(port)

servo_angle = stepper.get_servo_angle()
print('servo_angle: {}'.format(servo_angle))

angle_list_fwd = range(0,180,1)
angle_list_rev = angle_list_fwd[::-1] 
angle_list = angle_list_fwd + angle_list_rev


while True:
    for i, angle in enumerate(angle_list):
        print('i: {}, angle: {}'.format(i, angle))
        stepper.set_servo_angle(angle)
        time.sleep(0.01)


