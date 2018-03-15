from autostep import Autostep
import time

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_jog()
stepper.enable()

stepper.set_position(0.0)

pos_list = [180.0, 360.0, 0.0]

for pos in pos_list:
    stepper.move_to(pos)  
    time.sleep(2.0)

