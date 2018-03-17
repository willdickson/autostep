from __future__ import print_function
import time
import numpy as np
from autostep import Autostep

port = '/dev/ttyACM0'
dt = 0.5

velo_array = np.linspace(100,500,10)

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_max()
stepper.enable()


stepper.run(0.0)  
time.sleep(dt)

for i, velo in enumerate(velo_array): 
    print(i, velo)
    stepper.run(velo)  
    time.sleep(dt)

stepper.run(0.0)  
