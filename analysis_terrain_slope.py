import numpy as np
import matplotlib.pyplot as plt
from subfunctions import *


def bisection(upper, lower, terrain_angle, crr, rover, planet,):
    lowerValue = min(F_net(lower, terrain_angle, rover, planet, crr))   # min used to convert set into a scalar
    upperValue = min(F_net(upper, terrain_angle, rover, planet, crr))
    if upperValue * lowerValue > 0:  # root bracket check
        return 'NAN'

    error = 1.0
    errorCap = 0.0001
    iteration = 0
    iterationCap = 200

    while (error >= errorCap) and (iteration <= iterationCap):
        midOmegaValue = (min(upper) + min(lower)) / 2   # float representation of midpoint
        lowerValue = min(F_net(lower, terrain_angle, rover, planet, crr))
        upperValue = min(F_net(upper, terrain_angle, rover, planet, crr))
        midOmega = numpy.array(([midOmegaValue]*int(len(terrain_angle))))
        midValue = min(F_net(midOmega, terrain_angle, rover, planet, crr))

        if (lowerValue * midValue) < 0:
            upper = midOmega
        elif (lowerValue * midValue) > 0:
            lower = midOmega
        elif (lowerValue * midValue) == 0:
            return midOmega

        if iteration != 0:   # relative error check on 2nd iteration forward
            error = abs((oldVal - midOmegaValue) / midOmegaValue)

        oldVal = midOmegaValue
        iteration += 1

    return midOmegaValue


crr = 0.2
slope_array_deg = np.linspace(-10, 35, 25)
shape = np.shape(slope_array_deg)
v_max = np.zeros(shape)
radius = rover['wheel_assembly']['wheel']['radius']

for index, slope in enumerate(slope_array_deg):
    terrain_num = float(slope)  # Value of terrain angle as a float
    terrain_angle = numpy.array([terrain_num])  # Angle value in array class
    omegaLow = numpy.array([0.0])  # low omega in an array to be able to use subfunctions
    omegaHigh = numpy.array([3.8])
    omega = bisection(omegaHigh, omegaLow, terrain_angle, crr, rover, planet)
    try:
        v_max[index] = omega * radius
    except TypeError:   # for 'NAN' responses
        v_max[index] = omega

plt.plot(slope_array_deg, v_max, '-b')
plt.xlabel('Slope [degrees]')
plt.ylabel('Maximum Velocity [m/s]')
plt.title('Slope Terrain Analysis')
plt.show()

