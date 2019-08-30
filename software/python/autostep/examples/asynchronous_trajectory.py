import time
import scipy
import matplotlib.pyplot as plt

from autostep import Autostep
from autostep import AsynchronousTrajectory
from autostep.utility import get_ramp

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_16') 
stepper.set_fullstep_per_rev(200)
stepper.set_gear_ratio(1.0)

stepper.set_jog_mode_params({'speed': 200,  'accel': 1000, 'decel': 1000})
stepper.set_max_mode_params({'speed': 1000,  'accel': 30000, 'decel': 30000})
stepper.set_move_mode_to_jog()
stepper.enable()

traj = AsynchronousTrajectory(stepper)
dt = traj.dt

p0 = 0.0  
p1 = 360.0
vmax = 100.0
accel = 50.0

pos = get_ramp(p0,p1,vmax,accel,dt)
t = scipy.arange(pos.shape[0])*dt

if 0:
    plt.plot(t,pos)
    plt.grid('on')
    plt.xlabel('(sec)')
    plt.ylabel('pos')
    plt.show()

traj.run(pos,set_pos_to_start=True)

done = False
while not done:
    state = traj.state
    done = state['done']
    #print('done = {done}, t = {t:0.1f}, pos = {pos:0.1f}'.format(**state))
    time.sleep(0.1)

data = traj.data


plt.plot(data['t'], data['setp'], 'r')
plt.plot(data['t'], data['pos'], 'b')
plt.grid(True)
plt.xlabel('(sec)')
plt.ylabel('pos')
plt.show()

