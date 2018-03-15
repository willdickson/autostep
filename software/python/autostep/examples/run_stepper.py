from autostep import Autostep

port = '/dev/ttyACM0'

stepper = Autostep(port)
stepper.set_step_mode('STEP_FS_128') 
stepper.set_fullstep_per_rev(200)
stepper.set_move_mode_to_jog()
stepper.enable()
stepper.run(100.0)  # Run at 100 deg/sec

