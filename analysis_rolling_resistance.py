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
    iterationCap = 300

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


slope = 0.0
Crr_array = np.linspace(0.01, 0.4, 25)
shape = np.shape(Crr_array)
v_max = np.zeros(shape)
radius = rover['wheel_assembly']['wheel']['radius']

for index, Crr in enumerate(Crr_array):
    terrain_num = float(Crr)  # float representation of angle
    terrain_angle = numpy.array([0])  # Array representation of angle
    omegaLow = numpy.array([0.0])  # low omega represented in an array
    omegaHigh = numpy.array([3.8])   # high omega as a numpy array
    float_crr = float(Crr)
    omega = bisection(omegaHigh, omegaLow, terrain_angle, float_crr, rover, planet)
    try:
        v_max[index] = omega * radius
    except TypeError:   # for 'NAN' responses
        v_max[index] = omega

plt.plot(Crr_array, v_max, '-r')
plt.xlabel('Rolling Resistance Coefficient')   # not sure if this is unit-less or not
plt.ylabel('Maximum Velocity [m/s]')
plt.title('Rolling Resistance Analysis')
plt.show()