from __future__ import print_function
import serial
import atexit
import json



class Autostep(serial.Serial):

    Baudrate = 115200
    BusyWaitSleepDt = 0.05
    DefaultTimeout = 10.0
    DefaultResetSleep = 0.0

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


    def atexit_cleanup(self):
        pass


class AutostepException(Exception):
    pass

# ---------------------------------------------------------------------------------------
if __name__ == '__main__':

    import time
    import numpy
    import matplotlib.pyplot as plt

    port = '/dev/ttyACM0'

    stepper = Autostep(port)
    stepper.set_step_mode('STEP_FS_128') 
    stepper.set_move_mode_to_jog()

    stepper.enable()
    stepper.autoset_position()

    #stepper.move_to(0.0)
    #time.sleep(5.0)

    param = { 
            'amplitude': 90.0,
            'period':  4,
            'phase':  90.0,
            'offset': 100.0, 
            'num_cycle': 2 
            }
    data = stepper.sinusoid(param)
    stepper.busy_wait()

    data = numpy.array(data)
    tsec = data[:,0]
    angl = data[:,1]
    setp = data[:,2]
    sens = data[:,3]

    plt.plot(tsec,angl,'b')
    plt.plot(tsec,setp,'r')
    plt.plot(tsec,sens,'g')
    plt.show()
    

    #num =  50 
    #angle_array = numpy.concatenate((numpy.linspace(5,355,num), numpy.linspace(355,5,num)))

    #sensor_angle_list = []
    #sensor_volt_list = []

    #for i, angle in enumerate(angle_array):
    #    stepper.move_to(angle)
    #    stepper.busy_wait()
    #    sensor_angle = stepper.get_position_sensor()
    #    sensor_volt = stepper.get_voltage_sensor()
    #    sensor_angle_list.append(sensor_angle)
    #    sensor_volt_list.append(sensor_volt)
    #    print('{0}: {1:1.2f} {2:1.2f} {3:1.3f}'.format(i, angle, sensor_angle,sensor_volt))


    #stepper.move_to(0.0)
    #sensor_angle_array = numpy.array(sensor_angle_list)

    #fit = numpy.polyfit(angle_array, sensor_angle_array,1)
    #fit_angle_array = numpy.linspace(angle_array.min(), angle_array.max(), 500)
    #fit_sensor_angle_array = numpy.polyval(fit,fit_angle_array)
    #
    #plt.plot(angle_array, sensor_angle_list, 'o')
    #plt.plot(fit_angle_array, fit_sensor_angle_array, 'r')
    #plt.grid('on')
    #plt.xlabel('motor position (deg)')
    #plt.ylabel('em3242 sensor (deg)')
    #plt.show()









