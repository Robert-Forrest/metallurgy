from collections.abc import Iterable

import numpy as np

import metallurgy as mg
from .alloy import Alloy


def ideal_entropy(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [ideal_entropy(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    total_ideal_entropy = 0
    for element in alloy.elements:
        total_ideal_entropy += alloy.composition[element] * np.log(
            alloy.composition[element]
        )

    return -total_ideal_entropy


def ideal_entropy_xia(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [ideal_entropy_xia(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    cube_sum = 0
    for element in alloy.elements:
        cube_sum += (
            alloy.composition[element]
            * mg.periodic_table.elements[element]["atomic_volume"]
        )

    ideal_entropy = 0
    for element in alloy.composition:
        ideal_entropy += alloy.composition[element] * np.log(
            (
                alloy.composition[element]
                * mg.periodic_table.elements[element]["atomic_volume"]
            )
            / cube_sum
        )

    return -ideal_entropy


def mismatch_entropy(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mismatch_entropy(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if len(alloy.elements) == 1:
        return 0.0

    diameters = {}
    for element in alloy.composition:
        if mg.periodic_table.elements[element]["radius"] is None:
            return None

        diameters[element] = mg.periodic_table.elements[element]["radius"] * 2

    sigma_2 = 0
    for element in alloy.composition:
        sigma_2 += alloy.composition[element] * (diameters[element] ** 2)

    sigma_3 = 0
    for element in alloy.composition:
        sigma_3 += alloy.composition[element] * (diameters[element] ** 3)

    y_3 = (sigma_2**3) / (sigma_3**2)

    y_1 = 0
    y_2 = 0

    for i in range(len(alloy.elements) - 1):
        for j in range(i + 1, len(alloy.elements)):
            element = alloy.elements[i]
            otherElement = alloy.elements[j]

            y_1 += (
                (diameters[element] + diameters[otherElement])
                * ((diameters[element] - diameters[otherElement]) ** 2)
                * alloy.composition[element]
                * alloy.composition[otherElement]
            )

            y_2 += (
                diameters[element]
                * diameters[otherElement]
                * ((diameters[element] - diameters[otherElement]) ** 2)
                * alloy.composition[element]
                * alloy.composition[otherElement]
            )

    y_1 /= sigma_3

    y_2 *= sigma_2 / (sigma_3**2)

    packing_fraction = 0.64
    zeta = 1.0 / (1 - packing_fraction)

    return (
        ((3.0 / 2.0) * ((zeta**2) - 1) * y_1)
        + ((3.0 / 2.0) * ((zeta - 1) ** 2) * y_2)
        - (1 - y_3) * (0.5 * (zeta - 1) * (zeta - 3) + np.log(zeta))
    )


def mixing_entropy(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_entropy(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    ideal = ideal_entropy(alloy)
    mismatch = mismatch_entropy(alloy)

    if ideal is not None and mismatch is not None:
        return ideal + mismatch
    else:
        return None
