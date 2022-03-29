import numpy as np
import metallurgy as mg
from .alloy import Alloy


def calculate_average_size_ratio(composition):
    if(len(composition) > 1):
        elements = []
        for element in composition:
            elements.append(element)
        elementPairs = [(a, b) for idx, a in enumerate(elements)
                        for b in elements[idx + 1:]]

        average_ratio = 0
        for pair in elementPairs:
            tmpComposition = {}
            subComposition = 0
            for element in pair:
                subComposition += composition[element]
            for element in pair:
                tmpComposition[element] = composition[element] / subComposition

            radii = [tmpComposition[pair[0]] * calculate_radius(pair[0], tmpComposition),
                     tmpComposition[pair[1]] * calculate_radius(pair[0], tmpComposition)]
            maxR = max(radii)
            minR = min(radii)
            ratio = 1 - np.abs((maxR - minR) / maxR)

            average_ratio += subComposition * ratio

        return average_ratio / len(elementPairs)
    else:
        return 1


def calculate_radius_gamma(alloy):
    if not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    maxR = 0
    minR = 1000

    meanR = 0
    for element in alloy.elements:
        meanR += alloy.composition[element] * \
            mg.periodic_table.dict[element]['radius']

    for element in alloy.elements:
        r = mg.periodic_table.dict[element]['radius']
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
    if not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    meanR = 0
    for element in alloy.elements:
        meanR += alloy.composition[element] * \
            mg.periodic_table.dict[element]['radius']

    lattice_distortion = 0
    for i in range(len(alloy.elements) - 1):
        for j in range(i + 1, len(alloy.elements)):
            element = alloy.elements[i]
            otherElement = alloy.elements[j]

            radiusA = alloy.composition[element] * \
                mg.periodic_table.dict[element]['radius']
            radiusB = alloy.composition[element] * \
                mg.periodic_table.dict[otherElement]['radius']

            lattice_distortion += (alloy.composition[element] * alloy.composition[otherElement] * np.abs(
                radiusA + radiusB - 2 * meanR)) / (2 * meanR)

    return lattice_distortion
