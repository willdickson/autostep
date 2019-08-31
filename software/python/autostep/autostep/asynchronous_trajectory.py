from __future__ import print_function
import threading
import copy
import scipy
import scipy.interpolate


class AsynchronousTrajectory(object):
    """
    Implements an asynchronous trajectory tracker where the control loop for tracking the
    trajectory is run in a separate thread. 

    # Create the tracjectory handler
    traj = AsynchronousTrajectory(stepper)

    # Run atracjectory (does not b_lock)
    traj.run(pos)

    #  Can get state information while running from traj.state
    done = False

    while not done:

        state = traj.state

        # 'done' indicates whether or not trajectory is complete
        done = state['done']

        # 't' gives the elapsed time for the trajectory
        t = state['t']

        # 'pos' gives the current position of the motor 
        pos = state['pos']

        # 'setp' gives the current setpoint position of the motor
        setp = state['setp']


    # When trajectory is complete can access stored arrays of trajectory data from traj.data
    data = traj.data['t']     # array of trajectory time points
    data = traj.data['pos']   # array of trajctory positions
    data = traj.data['setp']  # array of trajctory setpt position 

    """

    def __init__(self,dev,pos_tol=2.0):
        self.dev = dev
        self.pos_tol = pos_tol
        self.dt = dev.TrajectoryDt 
        self._lock = threading.Lock()
        self._state = {}
        self._data = {}
        self._reset()

    def _reset(self):
        self._reset_state()
        self._reset_data()

    def _reset_state(self):
        with self._lock:
            pos = self.dev.get_position()
            self._state = {
                    't'    : 0.0,
                    'pos'  : pos,
                    'setp' : pos,
                    'done' : True,
                    }


    def _reset_data(self):
        with self._lock:
            self._data = {
                    't'    : [self._state['t']],
                    'pos'  : [self._state['pos']],
                    'setp' : [self._state['setp']],
                    }

    @property
    def done(self):
        with self._lock:
            done = self._state['done']
        return done


    @property
    def state(self):
        with self._lock:
            state = dict(self._state)
        return state


    @property
    def data(self):
        with self._lock:
            if self._state['done']:
                data = self._data
            else:
                data = None
        return data


    def _motion_data_cb(self, t, pos, setp):
        with self._lock:
            # Update state
            self._state['t'] = t
            self._state['pos'] = pos
            self._state['setp'] = setp

            # Update _data arrays
            self._data['t'].append(t)
            self._data['pos'].append(pos)
            self._data['setp'].append(setp)


    def _motion_done_cb(self):
        with self._lock:
            self._state['done'] = True
            self.dev.set_move_mode_to_jog()


    def run(self, pos_array, set_pos_to_start=False):
        """
        Run a trajectory.

        pos_array  = array of desired trajectory positions specified specified at the 
        trajectory handlers time step dt

        set_pos_to_start = flag which specifies whether or not the position of the motor


        """
        pos_array = scipy.array(pos_array)
        vel_array = scipy.zeros(pos_array.shape)
        vel_array[1:] = (pos_array[1:] - pos_array[:-1])/self.dt 

        if set_pos_to_start:
            self.dev.set_position(pos_array[0])

        pos = self.dev.get_position()
        if abs(pos - pos_array[0]) > self.pos_tol:
            raise(RuntimeError, 'current pos is > pos_tol from pos_array start')

        t = self.dt*scipy.arange(0,pos_array.shape[0])
        t_done = t[-1] 

        pos_array_func = scipy.interpolate.interp1d(t,pos_array,kind='linear')
        vel_array_func = scipy.interpolate.interp1d(t,vel_array,kind='linear')

        thread_args = [t_done, pos_array_func, vel_array_func, False, self._motion_data_cb, self._motion_done_cb] 
        motion_thread = threading.Thread(target=self.dev.run_trajectory, args=thread_args)
        motion_thread.daemon = True

        self._reset_state()
        self._reset_data()

        with self._lock:
            self._state['done'] = False
            self.dev.set_move_mode_to_max()

        motion_thread.start()



