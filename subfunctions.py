import numpy


def get_mass(rover):    # Austin
    #Rover dictionary data structure containing rover paramters
    """Computes the total mass of the rover. Uses information in the rover dict"""


def get_gear_ratio(speed_reducer):  # Austin
    #speed_reducer must be a dictionary specifying speed reducer paramters

    """Returns the speed reduction ratio for the speed reducer based on speed_reducer dict."""


def tau_dcmotor(omega, motor):  # Davis
    # Omega must be numpy array
    # Motor must be a dictionary specifying motor parameter
    # Must return a numpy array
    """Returns the motor shaft torque when given motor shaft speed and a dictionary containing important
    specifications for the motor. """

    valueCheck = (type(omega) not in (numpy.ndarray, float, int)) or (motor is not dict)
    if valueCheck:
        raise TypeError('Incorrect parameters for tau_dcmotor')

    if omega > motor['speed_noload']:
        torque = 0 * omega
    elif omega < 0:
        torque = motor['torque_stall'] * omega
    else:
        torque = motor['torque_stall'] - ((motor['torque_stall'] - motor['torque_noload']) / motor['speed_noload']) * omega

    return torque


def F_drive(omega, rover):  # Davis
    """Returns the force applied to the rover by the drive systemgiven information about the drive system (
    wheel_assembly) and the motor shaft speed. """

    valueCheck = (type(omega) not in (numpy.ndarray, float, int)) or (rover is not dict)
    if valueCheck:
        raise TypeError("F_drive function error... incorrect parameter value")

    gear_ratio = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    torque_1wheel = tau * gear_ratio
    force_1wheel = torque_1wheel / rover['wheel_assembly']['wheel']['radius']
    force_total = force_1wheel * 6

    return force_total



def F_gravity():    # Asher
    """Returns the magnitude of the force component acting on the rover in the direction of its translational motiondue  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover properties."""


def F_rolling():    # Asher
    """Returns the magnitude of the force component acting on the rover in the direction of its translational motiondue  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover properties"""


def F_net():
    """Returns the magnitude of net force acting on the rover in the direction of its translational motion."""
    

# Rover dictionary structure
planet = {'g': 3.72}
power_subsys = {'mass': 90.0}   # Review later
science_payload = {'mass': 75.0}
chassis = {'mass': 659.0}
motor = {'torque_stall': 170.0, 'torque_noload': 0.0, 'speed_noload': 3.8, 'mass': 5.0}
speed_reducer = {'type': 'Type of speed reducer', 'diam_pinion': 0.04, 'diam_gear': 0.07, 'mass': 1.5}   # Review later
wheel = {'radius': 0.3, 'mass': 1.0}
wheel_assembly = {'wheel': wheel,
                  'speed_reducer': speed_reducer,
                  'motor': motor
                  }
rover = {'wheel_assembly': wheel_assembly,
         'chassis': chassis,
         'science_payload': science_payload,
         'power_subsys': power_subsys
         }

