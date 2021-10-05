from math import erf, cos, sin, pi
from numpy import vectorize, array
import numpy as np

#Austin
def get_mass(rover):
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

#Austin
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
        
    
#Davis
def tau_dcmotor(omega, motor): 
    # Omega must be numpy array
    # Motor must be a dictionary specifying motor parameter
    # Must return a numpy array
    """Returns the motor shaft torque when given motor shaft speed and a dictionary containing important
    specifications for the motor. """

    valueCheck = (type(omega) not in (np.ndarray, float, int)) or (type(motor) is not dict)
    if valueCheck is True:
        raise TypeError('Incorrect parameters for tau_dcmotor')

    if omega.any() > motor['speed_noload']:
        torque = 0 * omega
    elif omega.any() < 0:
        torque = motor['torque_stall'] * omega
    else:
        torque = motor['torque_stall'] - ((motor['torque_stall'] - motor['torque_noload']) / motor['speed_noload']) * omega

    return torque

#Davis
def F_drive(omega, rover):
    """Returns the force applied to the rover by the drive systemgiven information about the drive system (
    wheel_assembly) and the motor shaft speed. """

    valueCheck = (type(omega) not in (np.ndarray, float, int)) or (rover is not dict)
    if valueCheck:
        raise TypeError("F_drive function error... incorrect parameter value")

    gear_ratio = get_gear_ratio(rover['wheel_assembly']['speed_reducer'])
    tau = tau_dcmotor(omega, rover['wheel_assembly']['motor'])
    torque_1wheel = tau * gear_ratio
    force_1wheel = torque_1wheel / rover['wheel_assembly']['wheel']['radius']
    force_total = force_1wheel * 6

    return force_total


#is there only a single case?
#Or case 1 -> positive angle
#case 2 -> zero angle
#case 3 -> negative angle
#Asher
def F_gravity(terrain_angle, rover, planet):   
    """Returns the magnitude of the force component acting on the rover in the direction of its translational motiondue  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover properties."""

    #Validating input parameters
    if type(terrain_angle) is not list and type(rover) is not dict and type(planet) is not dict:
        raise Exception("planet and rover need to be dictionaries") 

    #Validating terrain_angle values
    for angle in terrain_angle:
        #Checking if integer or floating point number
        if type(angle) is not float and type(angle) is not int:
            raise Exception("Invalid input: terrain_angle invalid type")
        #Checking if angle within given bounds
        if angle > 75 or angle < -75:
            raise Exception("Invalid input: terrain_angle out of bounds")  

    #Mass of rover
    m = get_mass(rover)
    
    #Computing terrain angle in radians
    terrain_angle = terrain_angle * (pi / 180)    
    
    #Computing force of gravity, 
    Fgt = m * planet['g'] * sin(terrain_angle)
    
    return Fgt

#Asher
def F_rolling(omega, terrain_angle, rover, planet, Crr): 
    """Returns the magnitude of the force component acting on the rover in the direction of its translational motiondue  to  gravity  as  a  function  of  terrain  inclination  angle  and  rover properties"""
    array_r = array([1])
    array_f = array([1.0])
    #Validation A, same size vecotrs
    if len(omega) != len(terrain_angle):
        raise Exception("the input omega and terrain_angle must be the same size")

    #Validating terrain_angle values
    for angle in terrain_angle:
        #Checking if integer or floating point number
        if type(angle) is not type(array_r[0]) and type(angle) is not type(array_f[0]):
            raise Exception("Invalid input: terrain_angle invalid type")
        #Checking if angle within given bounds
        if angle > 75 or angle < -75:
            raise Exception("Invalid input: terrain_angle out of bounds")  
    
    #Validating terrain angle input
    if type(terrain_angle) is not int and type(terrain_angle) is not float and type(terrain_angle) is not type(array_r) and type(terrain_angle) is not list:
        raise Exception('terrain angle must be a scalar or vector')    

    #Checking if third and fourth inputs are dictionaries
    if type(rover) is not dict or type(planet) is not dict:
        raise Exception("planet and rover need to be dictionaries")

    #Validating Crr is numeric
    if type(Crr) is not float and type(Crr) is not int:
        raise Exception("Crr needs to be type int or float")

    #Validating that Crr is a positive scalar
    if Crr < 0:
        raise Exception("Crr needs to be positive")
    
    gear_ratio = get_gear_ratio(speed_reducer)
    m = get_mass(rover)
    
    omega_out = omega / gear_ratio
    v_rover = rover['wheel_assembly']['wheel']['radius'] * omega_out * 40

    terrain_angle = terrain_angle * (pi / 180)
        
    Fn = abs(m * planet['g'] * np.cos(terrain_angle)) #using abs because normal force always positive
    Frrs = Crr * Fn 
    vector = vectorize(erf) #allows python to compute erf of an array
        
    Frr = vector(v_rover) * Frrs

    return Frr

#Austin
def F_net(omega, terrain_angle, rover, planet, Crr):
    """Returns the magnitude of net force acting on the rover in the direction of its translational motion."""
    #Validating will occur within other functions, no need to repeat

    Fgt = F_gravity(terrain_angle, rover, planet)
    Frr = F_rolling(omega, terrain_angle, rover, planet, Crr)
    Fd = F_drive(omega, rover)

    return Fgt - Frr + Fd
        

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

