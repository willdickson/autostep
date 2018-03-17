from __future__ import print_function
from autostep import Autostep
import time

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_max()
stepper.enable()

stepper.set_position(0.0)

pos_list = [180.0, 360.0, 2*360, 4*360, 0.0]

for pos in pos_list:
    print(pos)
    stepper.move_to(pos)  
    stepper.busy_wait()

