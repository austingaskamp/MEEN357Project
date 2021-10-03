#Plot the following graphs in a 3 x 1 matplot lib array
#1. motor shaft speed (rad/s) vs motor shaft torque (N * m), torque on x axis
#2. motor power (W) vs. motor shaft torque (N * m), torque on x axis
#3. motor power (W) vs. motor shaft speed (rad/s), speed on x axis

from subfunctions import *
import matplotlib.pyplot as plt
import numpy

#Rover dictionary structure
planet = {'g': 3.72}

power_subsys = {'mass': 90.0}   # Review later

science_payload = {'mass': 75.0}

chassis = {'mass': 659.0}

motor = {'torque_stall': 170.0,
         'torque_noload': 0.0,
         'speed_noload': 3.8,
         'mass': 5.0}

speed_reducer = {'type': "Reverted",
                 'diam_pinion': 0.04,
                 'diam_gear': 0.07,
                 'mass': 1.5}   # Review later

wheel = {'radius': 0.3,
         'mass': 1.0}

wheel_assembly = {'wheel': wheel,
                  'speed_reducer': speed_reducer,
                  'motor': motor}

rover = {'wheel_assembly': wheel_assembly,
         'chassis': chassis,
         'science_payload': science_payload,
         'power_subsys': power_subsys
        }

omega = numpy.linspace(0, 3.8, 100)

torque = tau_dcmotor(omega, rover['wheel_assembly']['motor'])

plt.plot(omega, torque, '-b')
plt.show()
