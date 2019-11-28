from __future__ import print_function
import time
import numpy as np
from autostep import Autostep

port = '/dev/ttyACM0'
dt = 0.5
dt = 5.0

velo_array = np.linspace(100,500,10)
velo_array = np.array([10,20])

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_max()
stepper.enable()


stepper.run(0.0)  
time.sleep(1.0)

for i, velo in enumerate(velo_array): 
    print(i, velo)
    #stepper.run(velo)  
    stepper.run_with_feedback(velo)  
    time.sleep(dt)

stepper.run(0.0)  
