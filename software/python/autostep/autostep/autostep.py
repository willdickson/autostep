from __future__ import print_function
import serial
import atexit
import json
import time
import numpy as np
import matplotlib.pyplot as plt
import threading


class Autostep(serial.Serial):

    """
    Provides a serial interface to the Autostep firmware for controlling the
    LM6470 dSPIN motor driver (as implemented in the Sparkfun Autodriver).
    """

    Baudrate = 115200
    BusyWaitSleepDt = 0.05
    DefaultTimeout = 10.0
    DefaultResetSleep = 0.0
    DefaultGearRatio = 1.0
    AutosetPositionStartAngle = 5.0
    TrajectoryGain = 20.0
    TrajectoryDt = 0.005

    StepModeList = [
            'STEP_FS', 
            'STEP_FS_2',
            'STEP_FS_4',
            'STEP_FS_8',
            'STEP_FS_16',
            'STEP_FS_32',
            'STEP_FS_64',
            'STEP_FS_128'
            ]

    MoveModeKeys = ('speed', 'accel', 'decel')
    MoveModeUnits = {
            'speed': '(deg/sec)', 
            'accel': '(deg/sec**2)',
            'decel': '(deg/sec**2)',
            }

    KvalKeys = ('accel', 'decel', 'run', 'hold')

    OC_ThresholdList = [ 
            "OC_375mA",
            "OC_750mA",
            "OC_1125mA",
            "OC_1500mA",
            "OC_1875mA",
            "OC_2250mA",
            "OC_2625mA",
            "OC_3000mA",
            "OC_3375mA",
            "OC_3750mA",
            "OC_4125mA",
            "OC_4500mA",
            "OC_4875mA",
            "OC_5250mA",
            "OC_5625mA",
            "OC_6000mA",
            ]

    def __init__(self, port, timeout=DefaultTimeout, reset_sleep=DefaultResetSleep, debug=False):
        params = {'baudrate': self.Baudrate, 'timeout': timeout}
        super(Autostep,self).__init__(port,**params)
        time.sleep(reset_sleep)
        atexit.register(self.atexit_cleanup)
        self.lock = threading.Lock()
        self.lock.acquire()
        while self.inWaiting() > 0:
            val = self.read()
        self.lock.release()
        self.sensor_cal = None
        self.gear_ratio = self.DefaultGearRatio


    def set_gear_ratio(self,gear_ratio):
        """
        Set the gear ratio - can be used to adjust for geared load.
        """
        self.gear_ratio = gear_ratio

    def enable(self):
        """
        Enable motor. When enabled motor will be held in firmly in position.
        """
        cmd_dict = {'command': 'enable'}
        self.send_cmd(cmd_dict)


    def release(self):
        """
        Release motor.  Performs soft stop and them puts motor drive into a high impedance
        state so that not current flows through windings.
        """
        cmd_dict = {'command': 'release'}
        self.send_cmd(cmd_dict)


    def run(self, velocity):
        """
        Run motor and given velocity (deg/sec). Motor will run at this velocity until 
        given another command (e.g. soft_stop, etc.)
        """
        velocity_adj = velocity*self.gear_ratio
        cmd_dict = {'command': 'run', 'velocity': velocity_adj}
        self.send_cmd(cmd_dict)


    def run_with_feedback(self,velocity):
        """
        Run motor and given velocity (deg/sec). Motor will run at this velocity until 
        given another command (e.g. soft_stop, etc.)
        """
        velocity_adj = velocity*self.gear_ratio
        cmd_dict = {'command': 'run_with_feedback', 'velocity': velocity_adj}
        rsp = self.send_cmd(cmd_dict)
        return rsp['position']/self.gear_ratio


    def run_trajectory(self, t_done, position_func, velocity_func, disp=False, on_data_callback=None, on_done_callback=None):
        """
        Run trajectory given by position and velocity_functions
        """

        pos_init = position_func(0)
        vel_init = velocity_func(0)

        self.set_move_mode_to_jog()
        self.move_to(pos_init)
        self.busy_wait()
        
        self.set_move_mode_to_max()
        self.run(vel_init)

        pos_curr = pos_init 
        vel_curr = vel_init

        t_list = []
        pos_list = []
        pos_setpt_list = []

        t_start = time.time()
        t_last = t_start

        while True:
            t = time.time() - t_start
            if t > t_done:
                break

            dt = t - t_last
            pos_next = position_func(t)
            vel_next = velocity_func(t)
            t_last = t

            pos_pred = pos_curr + vel_curr*dt
            error = pos_next - pos_pred
            vel_curr = vel_next + self.TrajectoryGain*error
            pos_curr = self.run_with_feedback(vel_curr)

            if on_data_callback is None:
                t_list.append(t)
                pos_list.append(pos_pred)
                pos_setpt_list.append(pos_next)
            else:
                on_data_callback(t,pos_pred,pos_next)
            time.sleep(self.TrajectoryDt)

            if disp:
                print('{:1.2f}, {:1.2f}, {:1.2f}'.format(t, pos_next, pos_pred))

        self.set_move_mode_to_jog()
        self.run(0.0)

        if on_done_callback is not None:
            on_done_callback()

        if on_data_callback is None:
            return  np.array(t_list), np.array(pos_list), np.array(pos_setpt_list) 


    def sinusoid(self, param, on_data_callback=None, on_done_callback=None): 
        """
        Run sinusoidal trajectory with given amplitude, period, phase, offest and number of cycles.
        """
        param_adj = dict(param)
        param_adj['amplitude'] = param_adj['amplitude']*self.gear_ratio
        param_adj['offset'] = param_adj['offset']*self.gear_ratio

        cmd_dict = {'command': 'sinusoid'};
        sinusoid_keys = ['amplitude', 'period', 'phase', 'offset', 'num_cycle']
        for key in sinusoid_keys:
            cmd_dict[key] = param_adj[key]
        rsp_dict = self.send_cmd(cmd_dict)

        data_list = []
        while True:
            self.lock.acquire()
            dat_json = self.readline()
            self.lock.release()
            dat_json = dat_json.strip()
            dat_dict = json.loads(dat_json.decode())
            if on_data_callback is None:
                if dat_dict:
                    data_list.append([dat_dict['t'], dat_dict['p'], dat_dict['s'], dat_dict['m']])
                else:
                    break
            else:
                if dat_dict:
                    elapsed_time = dat_dict['t']
                    position = dat_dict['p']
                    setpoint = dat_dict['s']
                    sensor = dat_dict['m']
                    on_data_callback(elapsed_time, position, setpoint, sensor)
                else:
                    break

        if on_done_callback is not None:
            on_done_callback()

        if on_data_callback is None:
            return data_list


    def move_to_sinusoid_start(self, param):
        """
        Move to sinusoid start position
        """
        phase_rad = np.deg2rad(param['phase'])
        angle = param['amplitude']*np.sin(0 + phase_rad) + param['offset'] 
        self.move_to(angle)

    def move_to(self,position):
        """
        Move motor to specified position (deg). Motor will run until it reaches this position.
        """
        position_adj = position*self.gear_ratio
        cmd_dict = {'command': 'move_to', 'position': position_adj}
        self.send_cmd(cmd_dict)


    def move_to_fullsteps(self, position):
        """
        Move motor to specified position in fullsteps. Motor will run until it reaches this position.
        """
        cmd_dict = {'command': 'move_to_fullsteps', 'position': position}
        self.send_cmd(cmd_dict)


    def move_to_microsteps(self, position):
        """
        Move motor to specified position in microsteps. Motor will run until it reaches this position.
        """
        cmd_dict = {'command': 'move_to_microsteps', 'position': position}
        self.send_cmd(cmd_dict)


    def soft_stop(self):
        """
        Perform soft stop - motor will stop using deceleration in current mode (jog or max).
        """
        cmd_dict = {'command': 'soft_stop'}
        self.send_cmd(cmd_dict)


    def hard_stop(self):
        """
        Perform hard stop - motor will stop as quickly as possible. Ignores deceleration settings.
        """
        cmd_dict = {'command': 'hard_stop'}
        self.send_cmd(cmd_dict)


    def is_busy(self):
        """
        Check if motor is busy performing a motion command
        """
        cmd_dict = {'command': 'is_busy'}
        rsp_dict = self.send_cmd(cmd_dict)
        return rsp_dict['is_busy']


    def busy_wait(self):
        """
        Wait unil current motion command is finshed.
        """
        while self.is_busy():
            time.sleep(self.BusyWaitSleepDt) 


    def set_move_mode_to_max(self):
        """
        Set movement mode to max - maximum acceleration/deceleration
        """
        cmd_dict = {'command': 'set_max_mode'}
        self.send_cmd(cmd_dict)


    def set_move_mode_to_jog(self):
        """
        Set movement mode to jog - softer acceleration/decelerat for positioning.
        """
        cmd_dict = {'command': 'set_jog_mode'}
        self.send_cmd(cmd_dict)


    def get_position(self):
        """
        Get the current position (deg) of the motor.
        """
        cmd_dict = {'command': 'get_position'}
        rsp_dict = self.send_cmd(cmd_dict)
        position_adj = rsp_dict['position']/self.gear_ratio
        return position_adj 

    
    def set_position(self, position):
        """
        Set the current motor position (deg). Note, not a motion command - just assigns 
        the current position of the motor to the given position.
        """
        position_adj = position*self.gear_ratio
        cmd_dict = {'command': 'set_position', 'position': position_adj}
        self.send_cmd(cmd_dict)


    def get_position_fullsteps(self):
        """
        Gets the current position of the motor in fullsteps
        """
        cmd_dict = {'command': 'get_position_fullsteps'}
        rsp_dict = self.send_cmd(cmd_dict)
        return rsp_dict['position']


    def get_position_microsteps(self):
        """
        Gets the current position of the motor in microsteps
        """
        cmd_dict = {'command': 'get_position_microsteps'}
        rsp_dict = self.send_cmd(cmd_dict)
        return rsp_dict['position']


    def get_position_sensor(self):
        """
        Gets the current position of the motor as given by the EM3242 angle sensor.
        """
        cmd_dict = {'command': 'get_position_sensor'}
        rsp_dict = self.send_cmd(cmd_dict)
        return rsp_dict['position']


    def get_voltage_sensor(self):
        """
        Gets the current voltage value fo the EM3242 angle sensor.
        """
        cmd_dict = {'command': 'get_voltage_sensor'}
        rsp_dict = self.send_cmd(cmd_dict)
        return rsp_dict['voltage']


    def autoset_position(self):
        """
        Automatically sets the motor position from the EM3242 angle sensor.
        """
        cmd_dict = {'command': 'autoset_position'}
        self.send_cmd(cmd_dict)


    def run_autoset_procedure(self):
        """
        Runs autoset procedure to ensure consistance between autoset position and
        saved sensor calibrations.
        """
        self.autoset_position()
        self.move_to(self.AutosetPositionStartAngle)
        self.busy_wait()
        self.autoset_position()


    def get_step_mode(self):
        """
        Get the current step_mode (e.g. STEP_FS, STEP_FS_2, ...)
        """
        cmd_dict = {'command': 'get_step_mode'}
        rsp_dict = self.send_cmd(cmd_dict)
        return rsp_dict['step_mode']


    def set_step_mode(self, step_mode):
        """
        Sets step mode used by the drive (mode should be in StepModeList).
        """
        cmd_dict = {'command': 'set_step_mode', 'step_mode': step_mode}
        self.send_cmd(cmd_dict)


    def send_cmd(self,cmd_dict):
        """ 
        Sends a command to the device.  Low-level method - command is specified 
        using command dictionary.

        """
        cmd_json = json.dumps(cmd_dict) + '\n'
        self.lock.acquire()
        self.write(cmd_json.encode())
        msg_json = self.readline()
        self.lock.release()
        msg_json = msg_json.strip()
        msg_dict = json.loads(msg_json.decode())
        if not msg_dict['success']==True:
            try:
                failure_info = msg_dict['message']
            except KeyError:
                failure_info = 'None' 
            exception_info = 'command: {0} failed, message: {1}'.format(cmd_dict['command'],failure_info) 
            raise AutostepException(exception_info)
        return msg_dict


    def have_calibraiton(self):
        """
        True/False based on existance of sensor calibration
        """
        if self.sensor_cal is None:
            return False
        else:
            return True


    def calibrate_sensor(self,num_pts=10,margin=1.5,plot_data=True,print_info=True):
        """
        Generate calibration for EM3242 sensor.
        """

        if print_info:
            print()
            print("Calibrating angle sensor, num_pts = {}".format(num_pts))
            print()

        self.sensor_cal = None

        self.enable()
        self.run_autoset_procedure()
        
        # Loop over calibration angles and get corresponding sensor angle
        calib_angle_array_tmp = np.linspace(margin,360.0-margin,num_pts)
        sense_angle_array_tmp = np.zeros(calib_angle_array_tmp.shape)

        self.set_move_mode_to_jog()
        self.move_to(calib_angle_array_tmp[0])
        self.busy_wait()

        self.set_move_mode_to_max()

        for i, calib_angle in enumerate(calib_angle_array_tmp):
            self.move_to(calib_angle)
            self.busy_wait()
            sense_angle = self.get_position_sensor()
            sense_angle_array_tmp[i] = sense_angle
            if print_info:
                calib_str = '{:3.3f}'.format(calib_angle)
                sense_str = '{:3.3f}'.format(sense_angle)
                info_dict = {
                        'count': '({}/{})'.format(i,num_pts),
                        'calib': '{:<6} {:>8}'.format('calib', calib_str),
                        'sense': '{:<6} {:>8}'.format('sense', sense_str),
                        }
                print('{count:<10s} {calib:>10s}   {sense:>10s}'.format(**info_dict))

        self.set_move_mode_to_jog()

        # Add back end points and pack in to nx2 array
        calib_angle_array = np.zeros((num_pts+2,))
        calib_angle_array[1:num_pts+1] = calib_angle_array_tmp
        calib_angle_array[num_pts+1] = 360.0

        sense_angle_array = np.zeros((num_pts+2,))
        sense_angle_array[1:num_pts+1] = sense_angle_array_tmp
        sense_angle_array[num_pts+1] = 360.0

        self.sensor_cal = np.array([sense_angle_array,calib_angle_array]).transpose() 

        if plot_data:
            plt.plot(calib_angle_array, sense_angle_array,'o')
            plt.xlabel('calibration angle (deg)')
            plt.ylabel('sensor angle (deg)')
            plt.grid('on')
            plt.show()


    def apply_sensor_calibration(self,value):
        """
        Applies sensor calibration - converts values measured by sensor to motor position in
        degrees. 
        """
        if self.sensor_cal is not None:
            return np.interp(value, self.sensor_cal[:,0], self.sensor_cal[:,1])
        else:
            return value


    def save_sensor_calibration(self,filename):
        """
        Saves sensor calibration (if it exists) to a file.
        """
        if self.sensor_cal is not None:
            np.savetxt(filename, self.sensor_cal)


    def load_sensor_calibration(self,filename):
        """
        Loads the sensor calibration from a file.
        """
        self.sensor_cal = np.loadtxt(filename)


    def clear_sensor_calibration(self):
        """
        Clears any existing sensor calibration data.
        """
        self.sensor_cal = None


    def get_fullstep_per_rev(self):
        """
        Get the fullsteps/revolution for the stepper motor.
        """
        cmd_dict = {'command': 'get_fullstep_per_rev'}
        rsp_dict = self.send_cmd(cmd_dict)
        return rsp_dict['fullstep_per_rev']


    def set_fullstep_per_rev(self,value):
        """
        Set the fullstep/revolution setting for the stepper motor.
        """
        int_value = int(value)
        if int_value <= 0:
            raise ValueError, 'fullstep_per_rev must > 0'
        cmd_dict = {'command': 'set_fullstep_per_rev', 'fullstep_per_rev': int_value}
        self.send_cmd(cmd_dict)


    def get_jog_mode_params(self):
        """
        Get the set of parameters used for 'jog' movement mode. 
        speed (deg/sec), accel (deg/sec**2) and decel  (deg/sec**2).
        """
        cmd_dict = {'command': 'get_jog_mode_params'}
        rsp_dict = self.send_cmd(cmd_dict)
        return {k:rsp_dict[k] for k in self.MoveModeKeys}


    def set_jog_mode_params(self,params):
        """
        Set the paramaters used for 'jog' movement mode. 
        speed (deg/sec), accel (deg/sec**2) and decel  (deg/sec**2).
        """
        cmd_dict = {k:params[k] for k in self.MoveModeKeys}
        cmd_dict['command'] = 'set_jog_mode_params'
        cmd_dict.update(params)
        self.send_cmd(cmd_dict)


    def get_max_mode_params(self):
        """
        Get the set of parameters used for 'max' movement mode. 
        speed (deg/sec), accel (deg/sec**2) and decel  (deg/sec**2).
        """
        cmd_dict = {'command': 'get_max_mode_params'}
        rsp_dict = self.send_cmd(cmd_dict)
        return {k:rsp_dict[k] for k in self.MoveModeKeys}


    def set_max_mode_params(self,params):
        """
        Set the paramaters used for 'max' movement mode. 
        speed (deg/sec), accel (deg/sec**2) and decel  (deg/sec**2).
        """
        cmd_dict = {k:params[k] for k in self.MoveModeKeys}
        cmd_dict['command'] = 'set_max_mode_params'
        self.send_cmd(cmd_dict)


    def get_kval_params(self):
        """
        Get the kval parameters. The kval parameters are coefficients
        which scale the sinewave amplitudes used for phase current control.

        Returns a dict with parameters accel, decel, run and hold.  Parameters
        have 0-255 value range. 
    
        """
        cmd_dict = {'command': 'get_kval_params'}
        rsp_dict = self.send_cmd(cmd_dict)
        return {k:rsp_dict[k] for k in self.KvalKeys}


    def set_kval_params(self,params):
        """
        Set the kval parameters. The kval parameters are coefficients
        which scale the sinewave amplitudes used for phase current control.

        Takes a dict with parameters accel, decel, run and hold.  Parameters
        have 0-255 value range. 
        """
        cmd_dict = {k:params[k] for k in self.KvalKeys}
        cmd_dict['command'] = 'set_kval_params'
        self.send_cmd(cmd_dict)


    def get_oc_threshold(self):
        """
        Get the overcurrent threshold. The overcurrent threshold set the current at which an
        overcurrent event (disable) occurs.
        """ 
        cmd_dict = {'command': 'get_oc_threshold'}
        rsp_dict = self.send_cmd(cmd_dict)
        return rsp_dict['threshold']


    def set_oc_threshold(self,threshold):
        """
        Set the overcurrent threshold. The overcurrent threshold set the current at which an
        overcurrent event (disable) occurs.

        The value must be in the OC_ThresholdList. 
        """
        if not threshold in self.OC_ThresholdList:
            raise ValueError, 'unknown oc_threshold'
        cmd_dict = {'command': 'set_oc_threshold', 'threshold': threshold}
        self.send_cmd(cmd_dict)

    
    def print_params(self):
        """
        Prints the stepper driver parameters.
        """
        fullstep_per_rev = self.get_fullstep_per_rev()
        step_mode = self.get_step_mode()
        oc_threshold = self.get_oc_threshold()
        jog_mode_params = self.get_jog_mode_params()
        max_mode_params = self.get_max_mode_params()
        kval_params = self.get_kval_params()

        print()
        print('Autostep Parameters')
        print('----------------------------')
        print()
        print('fullstep/rev:  {0}'.format(fullstep_per_rev))
        print('step mode:     {0}'.format(step_mode))
        print('oc threshold:  {0}'.format(oc_threshold))
        print()
        print('jog mode:')
        for k,v in jog_mode_params.iteritems():
            print('  {0}: {1} {2}'.format(k,v,self.MoveModeUnits[k]))
        print()
        print('max mode:')
        for k, v in max_mode_params.iteritems():
            print('  {0}: {1} {2}'.format(k,v,self.MoveModeUnits[k]))
        print()
        print('kvals (0-255): ')
        for k,v in kval_params.iteritems():
            print('  {0:<6} {1}'.format(k+':',v))
        print()


    def get_params(self):
        """
        Returns dictionary of driver parameters
        """
        fullstep_per_rev = self.get_fullstep_per_rev()
        step_mode = self.get_step_mode()
        oc_threshold = self.get_oc_threshold()
        jog_mode_params = self.get_jog_mode_params()
        max_mode_params = self.get_max_mode_params()
        kval_params = self.get_kval_params()
        params = {
                'fullstep_per_rev': fullstep_per_rev,
                'step_mode': step_mode,
                'oc_threshold': oc_threshold, 
                'jog_mode_params': jog_mode_params,
                'max_mode_params': max_mode_params,
                'kval_params': kval_params
                }
        return params


    def atexit_cleanup(self):
        pass


class AutostepException(Exception):
    pass

# ---------------------------------------------------------------------------------------
if __name__ == '__main__':


    port = '/dev/ttyACM0'
    cal_filename = 'sensor.cal'

    stepper = Autostep(port)
    stepper.set_step_mode('STEP_FS_128') 
    stepper.set_fullstep_per_rev(200)
    stepper.set_move_mode_to_max()
    stepper.enable()

    stepper.print_params()


    if 0:
        """
        Simple positioning move

        """
        stepper.set_move_mode_to_max()
        stepper.move_to(90.0)
        stepper.busy_wait()
        time.sleep(1.0)
        stepper.move_to(180.0)
        stepper.busy_wait()
        time.sleep(1.0)
        stepper.move_to(0.0)
        stepper.busy_wait()


    if 0:

        """
        Generate sensor calibration

        """

        stepper.calibrate_sensor(50)
        stepper.save_sensor_calibration(cal_filename)


    if 0:

        """
        Sinusoid test

        """

        stepper.run_autoset_procedure()
        stepper.load_sensor_calibration(cal_filename)
        stepper.set_move_mode_to_max()

        param = { 
                'amplitude': 90.0,
                'period':  1.2,
                'phase':  90.0,
                'offset': 100.0, 
                'num_cycle': 2 
                }

        vel = param['amplitude']*(2.0*np.pi/param['period'])
        acc = param['amplitude']*(2.0*np.pi/param['period'])**2
        print('vel: {0:1.3f}'.format(vel))
        print('acc: {0:1.3f}'.format(acc))

        data = stepper.sinusoid(param)
        stepper.busy_wait()

        data = np.array(data)
        tsec = data[:,0]
        angl = data[:,1]
        setp = data[:,2]
        sens = data[:,3]

        sens = stepper.apply_sensor_calibration(sens)

        angl_line, = plt.plot(tsec,angl,'b')
        setp_line, = plt.plot(tsec,setp,'r')
        sens_line, = plt.plot(tsec,sens,'g')
        plt.xlabel('time (s)')
        plt.ylabel('angle (deg)')
        plt.grid('on')
        line_list = [angl_line, setp_line, sens_line]
        label_list = 'driver', 'setpt', 'sensor'
        plt.figlegend(line_list, label_list, 'upper right')

        plt.figure(2)
        d_angl = (angl[1:] - angl[:-1])/(tsec[1:] - tsec[:-1])
        plt.plot(tsec[1:], d_angl)
        plt.xlabel('time (s)')
        plt.ylabel('angular velocity (deg/sec)')
        plt.grid('on')

        plt.figure(3)
        dd_angl = (d_angl[1:] - d_angl[:-1])/(tsec[2:] - tsec[1:-1])
        plt.plot(tsec[2:], dd_angl)
        plt.xlabel('time (s)')
        plt.ylabel('angular accel (deg/sec**2)')
        plt.grid('on')


        plt.show()









