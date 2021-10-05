import numpy
import matplotlib.pyplot as plt
from subfunctions import F_net, rover, planet


def bisection(lower, upper, terrain_angle, crr, rover, planet,):
    lowerValue = min(F_net(lower, terrain_angle, rover, planet, crr))
    upperValue = min(F_net(upper, terrain_angle, rover, planet, crr))
    if upperValue * lowerValue > 0:
        return 'NAN'

    error = 1.0
    errorCap = 0.001
    iteration = 0
    iterationCap = 200

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


Crr_array= numpy.linspace(0.01, 0.4, 25)
slope_array_deg = numpy.linspace(-10, 35, 25)
CRR, SLOPE = numpy.meshgrid(Crr_array, slope_array_deg)
shape = numpy.shape(CRR)
VMAX = numpy.zeros(shape)

for index, i in enumerate(CRR):
    for index2, j in enumerate(SLOPE):
        crr = float(CRR[index, index2])   # Value of crr used in F_net

        terrain_num = float(SLOPE[index, index2])   # Value of terrain angle used in F_net
        terrain_angle = numpy.array([terrain_num])   # Angle value repeated in array of same size as omega
        omegaLow = numpy.array(([0.0]))   # low omega repeated in array same size length as slope_array_deg
        omegaHigh = numpy.array(([3.8]))   # high omega in array same size as slope_array_deg
        VMAX[index, index2] = bisection(omegaLow, omegaHigh, terrain_angle, crr, rover, planet)

figure = plt.figure()
ax = figure.add_subplot(projection='3d')
ax.plot_surface(CRR, SLOPE, VMAX)
ax.set_xlabel('CRR')
ax.set_ylabel('angle')
ax.set_zlabel('omega')
print('hi')
