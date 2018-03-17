from __future__ import print_function
from autostep import Autostep

port = '/dev/ttyACM0'
stepper = Autostep(port)
stepper.set_max_mode_params({'speed': 1400, 'accel': 100000, 'decel': 100000})
stepper.print_params()
