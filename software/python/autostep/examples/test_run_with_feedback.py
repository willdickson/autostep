from __future__ import print_function
from autostep import Autostep
import time
import numpy as np
import matplotlib.pyplot as plt

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

#port = '/dev/ttyACM0'
#
#dev = Autostep(port)
#dev.set_step_mode('STEP_FS_128') 
##dev.set_fullstep_per_rev(200)
##dev.set_jog_mode_params({'speed': 100,  'accel': 1000, 'decel': 1000})
##dev.set_max_mode_params({'speed': 800,  'accel': 100000, 'decel': 100000})
##dev.set_move_mode_to_jog()
##dev.set_gear_ratio(1.0)
#dev.enable()
#dev.set_position(0.0)
#
#dt = 0.05
#period = 4.0
#num_cycle = 1
#stepper_amp = 30.0
#rcservo_amp = 80.0
#gain = 20.0
#
#num_step = int(period*num_cycle/dt)
#t_array = dt*np.arange(num_step)
#
#stepper_ang_array = stepper_amp*np.cos(2.0*np.pi*t_array/period)
#rcservo_ang_array = rcservo_amp*(1.0 + np.cos(2.0*np.pi*t_array/period)) 
#
#stepper_vel_array = np.zeros(stepper_ang_array.shape)
#stepper_vel_array[1:] = (stepper_ang_array[1:] - stepper_ang_array[:-1])/dt
#
#if 0:
#    plt.subplot(3,1,1)
#    plt.plot(t_array,stepper_ang_array,'b')
#    plt.ylabel('step (deg)')
#    plt.grid('on')
#    plt.subplot(3,1,2)
#    plt.plot(t_array,stepper_vel_array,'b')
#    plt.ylabel('step (vel)')
#    plt.grid('on')
#    plt.subplot(3,1,3)
#    plt.plot(t_array,rcservo_ang_array,'b')
#    plt.ylabel('rc (ang)')
#    plt.xlabel('t (sec)')
#    plt.grid('on')
#    plt.show()
#
#
## Move to initial position
##dev.set_servo_angle(rcservo_ang_array[0])
##dev.move_to(stepper_ang_array[0])
##dev.busy_wait()
#
## Set move mode to max for run with feedback
#dev.set_move_mode_to_max()
#
#zipped_motion_data = zip(t_array, stepper_ang_array, stepper_vel_array, rcservo_ang_array)
#
#stepper_vel_adj = 0
#
#stepper_ang_tru_list = []
#stepper_ang_err_list = []
#
#dev.run_with_feedback(10.0)
#time.sleep(5.0)
#dev.run(0)
#
#
##for motion_tuple in zipped_motion_data:
##
##    t, stepper_ang_set, stepper_vel_set, rcservo_ang_set = motion_tuple
##    #stepper_ang_tru, stepper_vel_tru = dev.run_with_feedback(stepper_vel_adj)
##    stepper_ang_tru, stepper_vel_tru = dev.run_with_feedback(10.0)
##    stepper_ang_est = stepper_ang_tru + stepper_vel_adj*dt
##    stepper_ang_err = stepper_ang_set - stepper_ang_est
##    #stepper_vel_adj = gain*stepper_ang_err + stepper_vel_set
##    stepper_vel_adj = stepper_vel_set
##    #stepper_vel_adj = gain*stepper_ang_err 
##
##    stepper_ang_tru_list.append(stepper_ang_tru)
##    stepper_ang_err_list.append(stepper_ang_err)
##
##    print('{:1.2f}, {:1.2f}, {:1.2f}'.format(stepper_vel_adj, stepper_vel_set, stepper_vel_tru))
##
##
##    #print('t: {:1.2f}, stepper_ang: {:1.2f}, stepper_vel: {:1.2f}, rcservo_ang: {:1.2f}'.format(*motion_tuple))
##    #print('adj: {:1.2f}'.format(stepper_vel_adj))
##    time.sleep(dt)
#
##dev.set_move_mode_to_jog()
##dev.move_to(0)  
##dev.busy_wait()
#
#stepper_ang_tru_array = np.array(stepper_ang_tru_list)
#stepper_ang_err_array = np.array(stepper_ang_err_list)
#
##plt.subplot(2,1,1)
##plt.plot(t_array,stepper_ang_array,'b')
##plt.plot(t_array,stepper_ang_tru_array,'r')
##plt.ylabel('angle (deg)')
##plt.grid(True)
##
##plt.subplot(2,1,2)
##plt.plot(t_array,stepper_ang_err_array,'b')
##plt.ylabel('error (deg)')
##plt.grid(True)
##plt.xlabel('t (sec)')
##plt.show()
