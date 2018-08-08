from __future__ import print_function
from autostep import Autostep
import time

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_jog()
stepper.set_gear_ratio(2.0)
stepper.enable()
stepper.set_position(0.0)


cnt = 0 
pos = 0
step = 180.0
num_step = 0

#while cnt < num_step:
#    pos += step 
#    cnt += 1
#    print(cnt, pos)
#    stepper.move_to(pos)  
#    stepper.busy_wait()
#    time.sleep(2.0)
#
#stepper.move_to(0)  
#stepper.busy_wait()

param = { 
        'amplitude': 90.0,
        'period':  5.0,
        'phase':  90.0,
        'offset': 0.0, 
        'num_cycle': 2 
        }

stepper.move_to_sinusoid_start(param)
stepper.busy_wait()
time.sleep(2.0)

print(stepper.get_position())

stepper.set_move_mode_to_max()
data = stepper.sinusoid(param)
stepper.busy_wait()
time.sleep(2.0)

stepper.set_move_mode_to_jog()
stepper.move_to(0)  
stepper.busy_wait()
