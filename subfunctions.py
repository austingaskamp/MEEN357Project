from math import erf, cos, sin, pi
from numpy import vectorize
import numpy

def get_mass(rover):    # Austin
    #Rover dictionary data structure containing rover paramters
    """Computes the total mass of the rover. Uses information in the rover dict"""
    #validating input is a dictionary
    if type(rover) is not dict:
        raise Exception("Invalid input: get_mass")

    else:
        #initialize mass to 0
        m = 0 
        #add wheel mass
        m += rover['wheel_assembly']['wheel']['mass']
        #add speed_reducer mass
        m += rover['wheel_assembly']['speed_reducer']['mass']
        #add moter mass 
        m += rover['wheel_assembly']['motor']['mass']
        #add chassis mass
        m += rover['chassis']['mass']
        #add science_payload mass
        m += rover['science_payload']['mass']
        #add power_subsys mass
        m += rover['power_subsys']['mass']

        return m


def get_gear_ratio(speed_reducer):  # Austin
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



def F_gravity(omega, terrain_angle, rover, planet, Crr):    # Asher
    """Returns the magnitude of the force component acting on the rover in the direction of its translational motiondue  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover properties."""
    array_r = array([])
    for i in range(len(terrain_angle)):
        if terrain_angle[i] > 75 or terrain_angle[i] < -75:
            raise Exception("terrain_angle needs to be below 75 and above -75 degrees")  
    if type(terrain_angle) is not int and type(terrain_angle) is not float and type(terrain_angle) is not type(array_r):
        raise Exception('terrain angle must be a scalar or vector')
    if type(rover) is not dict or type(planet) is not dict:
        raise Exception("planet and rover need to be dictionaries")   
        
    m = get_mass(rover)
    
    terrain_angle = terrain_angle* pi / 180    
    
    Fgt = m * planet[g] * sin(terrain_angle)
    
    return Fgt

def F_rolling(omega, terrain_angle, rover, planet, Crr):    # Asher
    """Returns the magnitude of the force component acting on the rover in the direction of its translational motiondue  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover properties"""
    array_r = array([])
    if len(omega) != len(terrain_angle):
        raise Exception("the input omega and terrain_angle must be the same size")
    for i in range(len(terrain_angle)):
        if terrain_angle[i] > 75 or terrain_angle[i] < -75:
            raise Exception("terrain_angle needs to be below 75 and above -75 degrees")
    if type(terrain_angle) is not int and type(terrain_angle) is not float and type(terrain_angle) is not type(array_r):
        raise Exception('terrain angle must be a scalar or vector')    
    if type(rover) is not dict or type(planet) is not dict:
        raise Exception("planet and rover need to be dictionaries")
    if type(Crr) is not float and type(Crr) is not int:
        raise Exception("Crr needs to be type int or float")
    if Crr < 0:
        raise Exception("Crr needs to be positive")
    
    Ng = get_gear_ratio(speed_reducer)
    m = get_mass(rover)
    
    omega_out = omega / Ng
    v_rover = rover[wheel_assembly][wheel][radius] * omega_out

    terrain_angle = terrain_angle* pi / 180
        
    
    Fn = m * planet[g] * cos(terrain_angle)
    Frrs = Crr * Fn
    vector = vectorize(erf)
    v_rover *= 40
        
    Frr = vector(v_rover)*Frrs
    return Frr

def F_net(omega, terrain_angle, rover, planet, Crr):
    array_r = array([])
    """Returns the magnitude of net force acting on the rover in the direction of its translational motion."""
    if len(omega) != len(terrain_angle):
        raise Exception("the input omega and terrain_angle must be the same size")
    for i in range(len(terrain_angle)):
        if terrain_angle[i] > 75 or terrain_angle[i] < -75:
            raise Exception("terrain_angle needs to be below 75 and above -75 degrees")
    if type(terrain_angle) is not int and type(terrain_angle) is not float and type(terrain_angle) is not type(array_r):
        raise Exception('terrain angle must be a scalar or vector')    
    if type(rover) is not dict or type(planet) is not dict:
        raise Exception("planet and rover need to be dictionaries")
    if type(Crr) is not float and type(Crr) is not int:
        raise Exception("Crr needs to be type int or float")
    if Crr < 0:
        raise Exception("Crr needs to be positive")
        

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

