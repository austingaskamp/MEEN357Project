import numpy as np
import matplotlib.pyplot as plt
from subfunctions import *

crr = 0.2
slope_array_deg = np.linspace(-10, 35, 25)
shape = np.shape(slope_array_deg)
v_max = np.zeros(shape)

for index, slope in slope_array_deg:
    terrain_num = float(slope)  # Value of terrain angle used in F_net
    terrain_angle = numpy.array([terrain_num] * int(len(slope_array_deg)))  # Angle value repeated in array of same size as omega
    omegaLow = numpy.array(([0.0] * int(len(slope_array_deg))))  # low omega repeated in array same size length as slope_array_deg
    omegaHigh = numpy.array(([3.8] * int(len(slope_array_deg))))