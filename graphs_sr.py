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


def get_gear_ratio(speed_reducer):
    """Computes the gear ratio of the speed reducer"""
    #speed_reducer must be a dictionary specifying speed reducer paramters
    
    #Validating input is a dictionary
    if type(speed_reducer) is not dict:
        raise Exception("Invalid input: get_gear_ratio")

    #Validating type field, should be reverted
    elif speed_reducer['type'].upper() != "REVERTED":
        raise Exception("Invalid input: invalid type for speed_reducer")

    #Performing gear ratio calculation after input has been validatied 
    else:
        d1 = speed_reducer['diam_pinion']
        d2 = speed_reducer['diam_gear']
        gear_ratio = (d2 / d1) ** 2
        return gear_ratio
        

Ng = get_gear_ratio(speed_reducer)

omega_dist = 3.8 / Ng

omega = numpy.linspace(0, 3.8, 100)

torque = tau_dcmotor(omega, rover['wheel_assembly']['motor']) * Ng
fig, (g1, g2, g3) = plt.subplots(3,1)

g1.plot(omega, torque, '-b')
g1.set_xlabel('Speed Reducer Torque (N*m)')
g1.set_ylabel('Speed Reducer Speed (rad/s)')
g1.grid(True)

x = arange(0, 170/ Ng,.5)
y = -(rover['wheel_assembly']['motor']['speed_noload'] / rover['wheel_assembly']['motor']['torque_stall']) * (x*Ng)**2 + rover['wheel_assembly']['motor']['speed_noload'] * (x*Ng)


g2.plot(x,y, '-b')
g2.set_xlabel('Speed Reducer Torque (N*m)')
g2.set_ylabel('Speed Reducer Power (W)')
g2.grid(True)
    
x = arange(0, 3.8 *Ng, .001)
y = -(rover['wheel_assembly']['motor']['speed_noload'] / rover['wheel_assembly']['motor']['torque_stall']) * (rover['wheel_assembly']['motor']['torque_stall'] - (rover['wheel_assembly']['motor']['torque_stall'] / rover['wheel_assembly']['motor']['speed_noload'])* (x/Ng))**2 + rover['wheel_assembly']['motor']['speed_noload'] * (rover['wheel_assembly']['motor']['torque_stall'] - (rover['wheel_assembly']['motor']['torque_stall'] / rover['wheel_assembly']['motor']['speed_noload'])* (x/Ng))


g3.plot(x,y, '-b')
g3.set_xlabel('Speed Reducer Speed (rad/s)')
g3.set_ylabel('Speed Reducer Power (W)')
g3.grid(True)

fig.tight_layout()
fig.show()