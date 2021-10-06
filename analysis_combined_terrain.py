import numpy
import matplotlib.pyplot as plt
from subfunctions import F_net, rover, planet


def bisection(lower, upper, terrain_angle, crr, rover, planet,):
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


Crr_array= numpy.linspace(0.01, 0.4, 25)
slope_array_deg = numpy.linspace(-10, 35, 25)
CRR, SLOPE = numpy.meshgrid(Crr_array, slope_array_deg)
shape = numpy.shape(CRR)
VMAX = numpy.zeros(shape)
radius = rover['wheel_assembly']['wheel']['radius']

for index, i in enumerate(CRR):
    for index2, j in enumerate(SLOPE):
        crr = float(CRR[index, index2])   # Value of crr used in F_net

        terrain_num = float(SLOPE[index, index2])   # Value of terrain angle used in F_net
        terrain_angle = numpy.array([terrain_num])   # Angle value represented as a 1d numpy array
        omegaLow = numpy.array(([0.0]))   # low omega represented in an array for the functions
        omegaHigh = numpy.array(([3.8]))   # high omega represented in an array for the functions
        omega = bisection(omegaLow, omegaHigh, terrain_angle, crr, rover, planet)
        try:
            VMAX[index, index2] = omega * radius
        except TypeError:   # for 'NAN' entries
            VMAX[index, index2] = omega

figure = plt.figure()
ax = figure.add_subplot(projection='3d')
ax.plot_surface(CRR, SLOPE, VMAX)
ax.set_xlabel('CRR')
ax.set_ylabel('Angle [degrees]')
ax.set_zlabel('Maximum Velocity [m/s]')
ax.set_title('Combined Analysis')
