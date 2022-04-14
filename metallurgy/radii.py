from collections.abc import Iterable

import numpy as np

import metallurgy as mg
from .alloy import Alloy


def radius_gamma(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [radius_gamma(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    maxR = 0
    minR = 1000

    meanR = 0
    for element in alloy.elements:
        meanR += alloy.composition[element] * \
            mg.periodic_table.elements[element]['radius']

    for element in alloy.elements:
        r = mg.periodic_table.elements[element]['radius']
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


def lattice_distortion(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [lattice_distortion(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    meanR = 0
    for element in alloy.elements:
        meanR += alloy.composition[element] * \
            mg.periodic_table.elements[element]['radius']

    tmp_lattice_distortion = 0
    for i in range(len(alloy.elements) - 1):
        for j in range(i + 1, len(alloy.elements)):
            element = alloy.elements[i]
            otherElement = alloy.elements[j]

            radiusA = alloy.composition[element] * \
                mg.periodic_table.elements[element]['radius']
            radiusB = alloy.composition[element] * \
                mg.periodic_table.elements[otherElement]['radius']

            tmp_lattice_distortion += (alloy.composition[element] * alloy.composition[otherElement] * np.abs(
                radiusA + radiusB - 2 * meanR)) / (2 * meanR)

    return tmp_lattice_distortion
