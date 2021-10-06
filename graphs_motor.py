#Plot the following graphs in a 3 x 1 matplot lib array
#1. motor shaft speed (rad/s) vs motor shaft torque (N * m), torque on x axis
#2. motor power (W) vs. motor shaft torque (N * m), torque on x axis
#3. motor power (W) vs. motor shaft speed (rad/s), speed on x axis

from subfunctions import *
import matplotlib.pyplot as plt
import numpy
from numpy import arange

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

torque = (tau_dcmotor(omega, rover['wheel_assembly']['motor'])) / 6
fig, (g1, g2, g3) = plt.subplots(3,1)

g1.plot(omega, torque, '-b')
g1.set_xlabel('Motor Shaft Torque (N*m)')
g1.set_ylabel('Motor Shaft Speed (rad/s)')
g1.grid(True)

x = arange(0, 170,.5)
y = (-(rover['wheel_assembly']['motor']['speed_noload'] / rover['wheel_assembly']['motor']['torque_stall']) * x**2 + rover['wheel_assembly']['motor']['speed_noload'] * x)/6


g2.plot(x,y, '-b')
g2.set_xlabel('Motor Shaft Torque (N*m)')
g2.set_ylabel('Motor Powerm (W)')
g2.grid(True)
    
x = arange(0, 3.8, .001)
y = (-(rover['wheel_assembly']['motor']['speed_noload'] / rover['wheel_assembly']['motor']['torque_stall']) * (rover['wheel_assembly']['motor']['torque_stall'] - (rover['wheel_assembly']['motor']['torque_stall'] / rover['wheel_assembly']['motor']['speed_noload'])* x)**2 + rover['wheel_assembly']['motor']['speed_noload'] * (rover['wheel_assembly']['motor']['torque_stall'] - (rover['wheel_assembly']['motor']['torque_stall'] / rover['wheel_assembly']['motor']['speed_noload'])* x))/6


g3.plot(x,y, '-b')
g3.set_xlabel('Motor Shaft Speed (rad/s)')
g3.set_ylabel('Motor Power (W)')
g3.grid(True)

fig.tight_layout()
fig.show()


