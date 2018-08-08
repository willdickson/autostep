from __future__ import print_function
import time
import scipy
import matplotlib.pyplot as plt
from autostep import Autostep


def get_period_and_amplitude(velocity, acceleration):

    period = 2.0*scipy.pi*velocity/acceleration
    amplitude = (velocity**2)/acceleration
    return period, amplitude

min_velocity = 100   # degree/second
max_velocity = 1000  # degree/second
num_velocity = 10    # degree/second
acceleration = 1500  # degree/second**2

velocity_array = scipy.linspace(min_velocity, max_velocity, 10)

period_list = []
amplitude_list = []

for i, velocity in enumerate(velocity_array):
    period, amplitude = get_period_and_amplitude(velocity, acceleration)
    print('{}: {:1.2f} {:1.2f} {:1.2f}'.format(i, velocity, period, amplitude))
    period_list.append(period)
    amplitude_list.append(amplitude)

plt.figure(1)
plt.subplot(211)
plt.title('Constant Acceleration = {:1.2f}(deg/sec**2)'.format(acceleration))
plt.plot(velocity_array, period_list,'-o')
plt.ylabel('period (sec)')
plt.grid('on')

plt.subplot(212)
plt.plot(velocity_array, amplitude_list,'-o')
plt.ylabel('amplitute (deg)')
plt.grid('on')

plt.xlabel('velocity (deg/sec)')
plt.show()


    
port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_jog()
stepper.set_gear_ratio(2.0)
stepper.enable()
stepper.set_position(0.0)

for i, velocity in enumerate(velocity_array):

    period, amplitude = get_period_and_amplitude(velocity, acceleration)

    print('cnt {}: vel: {:1.2f} per: {:1.2f} amp: {:1.2f}'.format(i, velocity, period, amplitude))

    param = { 
            'amplitude': amplitude,
            'period':  period,
            'phase':  90.0,
            'offset': 0.0, 
            'num_cycle': 2 
            }

    stepper.set_move_mode_to_jog()
    stepper.move_to_sinusoid_start(param)
    stepper.busy_wait()
    time.sleep(2.0)
    
    stepper.set_move_mode_to_max()
    data = stepper.sinusoid(param)
    stepper.busy_wait()
    time.sleep(2.0)

stepper.set_move_mode_to_jog()
stepper.move_to(0)  
stepper.busy_wait()
