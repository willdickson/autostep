from __future__ import print_function
import scipy
import matplotlib.pyplot as plt


def get_period_and_acceleration(velocity, amplitude):
    period = 2.0*scipy.pi*amplitude/velocity
    acceleration = ((2.0*scipy.pi/period)**2)*amplitude
    return period, acceleration


min_velocity = 100   # degree/second
max_velocity = 1000  # degree/second
num_velocity = 10    # degree/second
amplitude = 90.0     # degree

velocity_array = scipy.linspace(min_velocity, max_velocity, 10)

period_list = []
acceleration_list = []

for i, velocity in enumerate(velocity_array):
    period, acceleration = get_period_and_acceleration(velocity, amplitude)
    print('{}: {:1.2f} {:1.2f} {:1.2f}'.format(i, velocity, period, acceleration))
    period_list.append(period)
    acceleration_list.append(acceleration)

plt.figure(1)
plt.subplot(211)
plt.title('Constant Amplitude = {:1.2f} (deg)'.format(amplitude))
plt.plot(velocity_array, period_list,'-o')
plt.ylabel('period (sec)')
plt.grid('on')

plt.subplot(212)
plt.plot(velocity_array, acceleration_list,'-o')
plt.ylabel('acceleration (deg)')
plt.grid('on')

plt.xlabel('velocity (deg/sec)')
plt.show()
