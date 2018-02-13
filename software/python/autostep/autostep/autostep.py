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

    port = '/dev/ttyACM0'

    stepper = Autostep(port)
    stepper.set_move_mode_to_max()
    stepper.enable()
    stepper.set_position(0.0)


    for mode in Autostep.StepModeList:

        print('setting mode {0}'.format(mode))
        stepper.set_step_mode(mode)

        mode_tmp = stepper.get_step_mode()
        print('reading mode {0}'.format(mode_tmp))
        print()






