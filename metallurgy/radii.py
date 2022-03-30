import numpy as np
import metallurgy as mg
from .alloy import Alloy


def calculate_radius_gamma(alloy):
    if isinstance(alloy, list):
        return [calculate_radius_gamma(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    maxR = 0
    minR = 1000

    meanR = 0
    for element in alloy.elements:
        meanR += alloy.composition[element] * \
            mg.periodic_table.data[element]['radius']

    for element in alloy.elements:
        r = mg.periodic_table.data[element]['radius']
        if r > maxR:
            maxR = r
        if r < minR:
            minR = r

    rMinAvSq = (minR + meanR)**2
    rMaxAvSq = (maxR + meanR)**2
    rAvSq = meanR**2

    numerator = 1.0 - np.sqrt((rMinAvSq - rAvSq) / (rMinAvSq))
    denominator = 1.0 - np.sqrt((rMaxAvSq - rAvSq) / (rMaxAvSq))

    return numerator / denominator


def calculate_lattice_distortion(alloy):
    if isinstance(alloy, list):
        return [calculate_lattice_distortion(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    meanR = 0
    for element in alloy.elements:
        meanR += alloy.composition[element] * \
            mg.periodic_table.data[element]['radius']

    lattice_distortion = 0
    for i in range(len(alloy.elements) - 1):
        for j in range(i + 1, len(alloy.elements)):
            element = alloy.elements[i]
            otherElement = alloy.elements[j]

            radiusA = alloy.composition[element] * \
                mg.periodic_table.data[element]['radius']
            radiusB = alloy.composition[element] * \
                mg.periodic_table.data[otherElement]['radius']

            lattice_distortion += (alloy.composition[element] * alloy.composition[otherElement] * np.abs(
                radiusA + radiusB - 2 * meanR)) / (2 * meanR)

    return lattice_distortion
