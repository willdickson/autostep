from __future__ import print_function
from autostep import Autostep
import time

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.run(100)
time.sleep(2.0)
stepper.soft_stop()

