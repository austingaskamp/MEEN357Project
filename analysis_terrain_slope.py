import numpy as np
import matplotlib.pyplot as plt
from subfunctions import *

crr = 0.2
slope_array_deg = np.linspace(-10, 35, 25)
shape = np.shape(slope_array_deg)
v_max = np.zeros(shape)
