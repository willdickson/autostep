from __future__ import print_function
from autostep import Autostep
import time
import numpy as np
import matplotlib.pyplot as plt


def get_kinematics_func(step_period, step_amplitude, rc_period, rc_amplitude):
    """
    Simple sinusoidal kinematics for stepper and rc servo

    """

    def vel_func(t):
        return -(2.0*np.pi/step_period)*step_amplitude*np.sin(2.0*np.pi*t/step_period)
    
    def pos_func(t):
        return step_amplitude*np.cos(2.0*np.pi*t/step_period)

    def rc_func(t):
        return  rc_amplitude*(np.cos(2.0*np.pi*t/rc_period) + 1)

    return pos_func, vel_func, rc_func


# ---------------------------------------------------------------------------------
if __name__ == '__main__':

    port = '/dev/ttyACM0'

    gain = 5.0
    sleep_dt = 0.005
    
    step_period = 4.0
    step_amplitude = 45.0
    rc_period = 8.0
    rc_amplitude = 80.0
    t_end = 2*step_period 
    
    pos_set_func, vel_set_func, rc_set_func = get_kinematics_func(
            step_period,
            step_amplitude, 
            rc_period,
            rc_amplitude
            )
    
    dev = Autostep(port)
    dev.set_step_mode('STEP_FS_64') 
    dev.set_fullstep_per_rev(200)
    dev.set_gear_ratio(1.0)
    dev.set_jog_mode_params({'speed': 200,  'accel': 1000, 'decel': 1000})
    dev.set_max_mode_params({'speed': 1000,  'accel': 30000, 'decel': 30000})
    dev.set_move_mode_to_max()
    dev.enable()
    dev.print_params()
    dev.run(0.0)  
    
    t_start = time.time()
    t_last = t_start
    
    t_list = []
    pos_tru_list = []
    pos_set_list = []
    
    pos_last = pos_set_func(0)
    dev.set_position(pos_last)
    
    vel_last = vel_set_func(0) 
    dev.run(vel_last)
    
    done = False
    
    while not done:
        
        t = time.time() - t_start

        # Compute estimated position (since last update)
        pos_est = pos_last + (t-t_last)*vel_last

        # Get new setpoint values
        pos_set = pos_set_func(t)
        vel_set = vel_set_func(t)
        rc_set  = rc_set_func(t)
    
        # Caluculate position error and use to determine correction velocity
        pos_err = pos_set - pos_est
        vel_adj = vel_set + gain*pos_err

        # Set stepper to run at correction velocity and get current position
        pos_tru = dev.run_with_feedback(vel_adj,rc_set)

        # Save update time and position/velocity information from update
        t_last = t
        pos_last = pos_tru
        vel_last = vel_adj

        # Check if we are done
        if t >= t_end:
            done = True
        
        # Save data for plotting
        t_list.append(t)
        pos_tru_list.append(pos_tru)
        pos_set_list.append(pos_set)
    
        print('t: {:1.2f}, pos: {:1.2f}'.format(t,pos_tru))
        time.sleep(sleep_dt)
    
    dev.run(0.0)  
    
    
    # Plot results
    plt.plot(t_list, pos_tru_list,'.b')
    plt.plot(t_list, pos_set_list, 'r')
    plt.xlabel('t (sec)')
    plt.ylabel('ang (deg)')
    plt.grid(True)
    
    plt.show()




