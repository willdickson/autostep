from __future__ import print_function
from autostep import Autostep
import time
import numpy
import matplotlib.pyplot as plt

period = 12.0
num_cycle = 1
t_done = num_cycle*period
amp_list = [100.0,-90,-40, 30, 20]

def position_func(t,period=period,amp_list=amp_list):
    pos = 0.0
    for i, amp in enumerate(amp_list):
        const = 2.0*numpy.pi*float(i+1)/period
        pos += amp*numpy.cos(const*t)
    return pos

def velocity_func(t,period=period, amp_list=amp_list):
    vel = 0.0
    for i, amp in enumerate(amp_list):
        const = 2.0*numpy.pi*float(i+1)/period
        vel += -const*amp*numpy.sin(const*t)
    return vel


t_array = numpy.linspace(0,t_done,1000*num_cycle)
print(type(t_array)==numpy.ndarray)
pos_list = []
vel_list = []
for t in t_array:
    pos = position_func(t)
    vel = velocity_func(t)
    pos_list.append(pos)
    vel_list.append(vel)

pos_array = numpy.array(pos_list)
vel_array = numpy.array(vel_list)

plt.subplot(211)
plt.plot(t_array,pos_array)
plt.ylabel('angle (deg)')
plt.grid('on')
plt.subplot(212)
plt.plot(t_array,vel_array)
plt.ylabel('velocity (deg/sec)')
plt.xlabel('time (sec)')
plt.grid('on')
plt.show()

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_jog()
stepper.set_gear_ratio(2.0)
stepper.enable()
stepper.set_position(0.0)

t, pos, pos_setpt = stepper.run_trajectory(t_done,position_func,velocity_func) 

plt.plot(t,pos,'b')
plt.plot(t,pos_setpt, '.r')
plt.xlabel('time (sec)')
plt.ylabel('angle (deg)')
plt.grid('on')
plt.show()
