from __future__ import print_function
import serial
import atexit
import json
import time
import numpy as np
import matplotlib.pyplot as plt


class Autostep(serial.Serial):

    Baudrate = 115200
    BusyWaitSleepDt = 0.05
    DefaultTimeout = 10.0
    DefaultResetSleep = 0.0
    AutosetPositionStartAngle = 5.0

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

    def __init__(self, port, timeout=DefaultTimeout, reset_sleep=DefaultResetSleep, debug=False):
        """ Constructor
        """
        params = {'baudrate': self.Baudrate, 'timeout': timeout}
        super(Autostep,self).__init__(port,**params)
        time.sleep(reset_sleep)
        atexit.register(self.atexit_cleanup)
        while self.inWaiting() > 0:
            val = self.read()
        self.sensor_cal = None


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
        cmd_dict = {'command': 'run', 'velocity': velocity}
        self.send_cmd(cmd_dict)


    def sinusoid(self, param): 
        """
        Run sinusoidal trajectory with given amplitude, period, phase, offest and number of cycles.
        """
        cmd_dict = {'command': 'sinusoid'};
        sinusoid_keys = ['amplitude', 'period', 'phase', 'offset', 'num_cycle']
        for key in sinusoid_keys:
            cmd_dict[key] = param[key]
        rsp_dict = self.send_cmd(cmd_dict)

        data_list = []
        while True:
            dat_json = self.readline()
            dat_json = dat_json.strip()
            dat_dict = json.loads(dat_json.decode())
            if dat_dict:
                data_list.append([dat_dict['t'], dat_dict['p'], dat_dict['s'], dat_dict['m']])
            else:
                break
        return data_list
        

    def move_to(self,position):
        """
        Move motor to specified position (deg). Motor will run until it reaches this position.
        """
        cmd_dict = {'command': 'move_to', 'position': position}
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
        return rsp_dict['position']

    
    def set_position(self, position):
        """
        Set the current motor position (deg). Note, not a motion command - just assigns 
        the current position of the motor to the given position.
        """
        cmd_dict = {'command': 'set_position', 'position': position}
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
        self.write(cmd_json.encode())
        msg_json = self.readline()
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
        return np.interp(value, self.sensor_cal[:,0], self.sensor_cal[:,1])


    def save_sensor_calibration(self,filename):
        np.savetxt(filename, self.sensor_cal)


    def load_sensor_calibration(self,filename):
        self.sensor_cal = np.loadtxt(filename)


    def clear_sensor_calibration(self):
        self.sensor_cal = None


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
    stepper.set_move_mode_to_jog()
    stepper.enable()


    if False:

        """
        Generate sensor calibration

        """

        stepper.calibrate_sensor(50)
        stepper.save_sensor_calibration(cal_filename)


    if True:

        """
        Sinusoid test

        """

        stepper.run_autoset_procedure()
        stepper.load_sensor_calibration(cal_filename)
        stepper.set_move_mode_to_max()

        param = { 
                'amplitude': 30,
                'period':  1,
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
        plt.show()
    











