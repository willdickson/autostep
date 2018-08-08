from __future__ import print_function
from autostep import Autostep
import time

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.enable()
stepper.busy_wait()
