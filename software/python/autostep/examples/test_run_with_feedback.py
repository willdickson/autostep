from __future__ import print_function
from autostep import Autostep
import time
import numpy as np

port = '/dev/ttyACM0'

dev = Autostep(port)
dev.set_step_mode('STEP_FS_8') 
dev.set_fullstep_per_rev(200)
dev.set_jog_mode_params({'speed': 100,  'accel': 1000, 'decel': 1000})
dev.set_max_mode_params({'speed': 800,  'accel': 100000, 'decel': 100000})
dev.set_move_mode_to_jog()
dev.set_gear_ratio(1.0)
dev.enable()
dev.set_position(0.0)

dt = 0.01
period = 4.0
num_cycle = 4
stepper_amp = 30.0
rcservo_amp = 80.0
gain = 10.0

num_step = int(period*num_cycle/dt)
t = dt*np.arange(num_step)

stepper_ang_array = stepper_amp*cos(2.0*np.pi*t/period)
stepper_vel_array = stepper_amp*(2.0*np.pi/period)*sin(2.0*np.pi*t/period)
rcservo_ang_array = 80*(1.0 + cos(2.0*np.pi*t/period)) 

# Move to initial position
dev.set_servo_angle(servo_angle_array[0])
dev.move_to(stepper_angles[0])
dev.busy_wait()

# Set move mode to max for run with feedback
dev.set_move_mode_to_max()

zipped_motion_data = (t, stepper_ang_array, stepper_vel_array, rcservo_ang_array)

stepper_vel_adj = 0

for motion_tuple in zipped_motion_data:

    t, stepper_ang, stepper_vel, rc_servo_ang = motion_tuple
    stepper_ang_tru = dev.run_with_feedback(stepper_vel_adj, rcservo_ang)
    stepper_ang_err = steper_ang - stepper_ang_tru
    stepper_vel_adj = gain*stepper_ang_err + stepper_vel

    print('t: {:1.2f}, stepper_ang: {:1.2f}, stepper_vel: {:1.2f}, rcservo_ang: {:1.2f}'.format(motion_tuple))
    time.sleep(dt)

dev.set_move_mode_to_jog()
dev.move_to(0)  
dev.busy_wait()
