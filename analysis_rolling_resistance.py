import numpy as np
import matplotlib.pyplot as plt
from subfunctions import *


def bisection(upper, lower, terrain_angle, crr, rover, planet,):
    lowerValue = min(F_net(lower, terrain_angle, rover, planet, crr))
    upperValue = min(F_net(upper, terrain_angle, rover, planet, crr))
    if upperValue * lowerValue > 0:
        return 'NAN'

    error = 1.0
    errorCap = 0.0001
    iteration = 0
    iterationCap = 300

    while (error >= errorCap) and (iteration <= iterationCap):
        midOmegaValue = (min(upper) + min(lower)) / 2
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

        if iteration != 0:
            error = abs((oldVal - midOmegaValue) / midOmegaValue)

        oldVal = midOmegaValue
        iteration += 1

    return midOmegaValue


slope = 0.0
Crr_array = np.linspace(0.01, 0.4, 25)
shape = np.shape(Crr_array)
v_max = np.zeros(shape)

for index, Crr in enumerate(Crr_array):
    terrain_num = float(Crr)  # Value of terrain angle used in F_net
    terrain_angle = numpy.array([0])  # Angle value repeated in array of same size as omega
    omegaLow = numpy.array([0.0])  # low omega repeated in array same size length as slope_array_deg
    omegaHigh = numpy.array([3.8])
    float_crr = float(Crr)
    v_max[index] = bisection(omegaHigh, omegaLow, terrain_angle, float_crr, rover, planet)

plt.plot(Crr_array, v_max, '-r')
plt.xlabel('Rolling Resistance Coefficient')
plt.ylabel('Maximum Velocity')
plt.title('Rolling Resistance Analysis')
plt.show()
print('breakpoint')