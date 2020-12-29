from __future__ import print_function
from autostep import Autostep
import time

port = '/dev/ttyACM0'

stepper = Autostep(port)

servo_angle_0 = stepper.get_servo_angle()
servo_angle_1 = stepper.get_servo_angle_alt()
print(f'servo_angle_0: {servo_angle_0} and servo_angle_1: {servo_angle_1}')

angle_list_fwd = list(range(0,180,1))
angle_list_rev = angle_list_fwd[::-1] 
angle_list_0 = angle_list_fwd + angle_list_rev
angle_list_1 = angle_list_rev + angle_list_fwd


while True:
    for i, (angle_0, angle_1) in enumerate(zip(angle_list_0, angle_list_1)):
        print(f'i: {i}, angle_0: {angle_0}, angle_1: {angle_1}')
        stepper.set_servo_angle(angle_0)
        stepper.set_servo_angle_alt(angle_1)
        time.sleep(0.01)


