from __future__ import print_function
import time
import scipy
import matplotlib.pyplot as plt
from autostep import Autostep


def get_amplitude_and_acceleration(velocity, period):
    amplitude = velocity*period/(2.0*scipy.pi)
    acceleration = ((2.0*scipy.pi/period)**2)*amplitude
    return amplitude, acceleration

min_velocity = 100   # degree/second
max_velocity = 1000  # degree/second
num_velocity = 10    # degree/second
period = 3.0         # seconds

velocity_array = scipy.linspace(min_velocity, max_velocity, 10)

amplitude_list = []
acceleration_list = []

for i, velocity in enumerate(velocity_array):
    amplitude, acceleration = get_amplitude_and_acceleration(velocity, period)
    print('{}: {:1.2f} {:1.2f} {:1.2f}'.format(i, velocity, amplitude, acceleration))
    amplitude_list.append(amplitude)
    acceleration_list.append(acceleration)

plt.figure(1)
plt.subplot(211)
plt.title('Constant Period = {:1.2f} (sec)'.format(period))
plt.plot(velocity_array, amplitude_list,'-o')
plt.ylabel('amplitude (sec)')
plt.grid('on')

plt.subplot(212)
plt.plot(velocity_array, acceleration_list,'-o')
plt.ylabel('acceleration (deg)')
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

    amplitude, acceleration = get_amplitude_and_acceleration(velocity, period)

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
