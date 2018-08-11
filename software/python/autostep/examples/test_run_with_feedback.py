from __future__ import print_function
from autostep import Autostep
import time
import numpy

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_jog()
stepper.set_gear_ratio(2.0)
stepper.enable()
stepper.set_position(0.0)

num_steps = 20 
min_velo = 10
max_velo = 100

velo_array = numpy.linspace(min_velo, max_velo, num_steps)

for velo in velo_array:

    position = stepper.run_with_feedback(velo)
    print(velo, position)
    time.sleep(0.5)


stepper.set_move_mode_to_jog()
stepper.move_to(0)  
stepper.busy_wait()
