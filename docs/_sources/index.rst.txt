.. autostep documentation master file, created by
   sphinx-quickstart on Fri May 10 09:02:16 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Autostep: Stepper Motor Control  
===============================

.. image:: _static/steppers.png

Autostep provides hardware, firmware and software libraries which enable
USB/Serial control of stepper motors driven by the STMicro L6470 dSPIN stepper
motor driver.  This stepper motor driver IC can control a stepper motor from a 8-45V
supply at up to 3A,  communicates with the host microcontroller over an SPI
connection and can autonomously executes movement commands eliminating the need
for step counting etc.  The L4670 IC is available in convenient low development
boards such as the `Sparkfun Autodriver
<https://www.sparkfun.com/products/13752>`_. 

Autostep provides following components to facilitate use of this IC based stepper driver:

* **Hardware** for conveniently  connecting the `teensy 3.2
  <https://www.pjrc.com/store/teensy32.html>`_ development board to the
  `Sparkfun Autodriver <https://www.sparkfun.com/products/13752>`_

* **Firmware** for the `teensy 3.2 <https://www.pjrc.com/store/teensy32.html>`_ 
  which enables the stepper to be controlled via USB/Serial commands

* A **Python Library** which communicates with device firmware over USB/Serial and enables high
  level motion control

* A **ROS Package** enabling use of the autostep with Robot Operating System
  (ROS). 



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   hardware
   firmware
   installation
   quick_start
   api_reference
   ros




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
