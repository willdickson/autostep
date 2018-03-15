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
        'amplitude': 90.0,
        'period':  1.2,
        'phase':  90.0,
        'offset': 100.0, 
        'num_cycle': 2 
        }

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
