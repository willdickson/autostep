import numpy as np
import matplotlib.pyplot as plt
from autostep import Autostep

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_max()
stepper.enable()

param = { 
        'amplitude': 180.0,
        'period':  5.0,
        'phase':  90.0,
        'offset': 0.0, 
        'num_cycle': 2 
        }

vel = param['amplitude']*(2.0*np.pi/param['period'])
acc = param['amplitude']*(2.0*np.pi/param['period'])**2
print('vel: {0:1.2f}'.format(vel))
print('acc: {0:1.2f}'.format(acc))

data = stepper.sinusoid(param)
stepper.busy_wait()

data = np.array(data)
tsec = data[:,0]
angl = data[:,1]
setp = data[:,2]

angl_line, = plt.plot(tsec,angl,'b')
setp_line, = plt.plot(tsec,setp,'r')

plt.xlabel('time (s)')
plt.ylabel('angle (deg)')
plt.grid('on')
line_list = [angl_line, setp_line]
label_list = 'driver', 'setpt'
plt.figlegend(line_list, label_list, 'upper right')
plt.show()
