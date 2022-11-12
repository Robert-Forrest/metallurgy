"""Entropy related calculations"""

from typing import Union, List
from collections.abc import Iterable
from numbers import Number

import numpy as np

import metallurgy as mg


def ideal_entropy(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the ideal entropy of an alloy. See equation 4 of
    https://doi.org/10.1016/j.chemphys.2020.110898.

    :group: calculations.entropy

    Parameters
    ----------

    alloy
        The alloy for which to calculate the ideal entropy.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [ideal_entropy(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    total_ideal_entropy = 0
    for element in alloy.elements:
        total_ideal_entropy += alloy.composition[element] * np.log(
            alloy.composition[element]
        )

    return -total_ideal_entropy


def ideal_entropy_xia(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns Xia's ideal entropy of an alloy. See equation 8 of
    http://dx.doi.org/10.1063/1.2345259.

    :group: calculations.entropy

    Parameters
    ----------

    alloy
        The alloy for which to calculate Xia's ideal entropy.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [ideal_entropy_xia(a) for a in alloy]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    cube_sum = 0
    for element in alloy.elements:
        volume = mg.periodic_table.elements[element]["atomic_volume"]
        if volume is None:
            return None

        cube_sum += alloy.composition[element] * volume

    ideal_entropy_x = 0
    for element in alloy.composition:
        ideal_entropy_x += alloy.composition[element] * np.log(
            (
                alloy.composition[element]
                * mg.periodic_table.elements[element]["atomic_volume"]
            )
            / cube_sum
        )

    return -ideal_entropy_x


def mismatch_entropy(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the mismatch entropy of an alloy. See equation 2 of
    https://doi.org/10.2320/matertrans1989.41.1372.

    :group: calculations.entropy

    Parameters
    ----------

    alloy
        The alloy for which to calculate the mismatch entropy.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mismatch_entropy(a) for a in alloy]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    if alloy.num_elements == 1:
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
            other_element = alloy.elements[j]

            y_1 += (
                (diameters[element] + diameters[other_element])
                * ((diameters[element] - diameters[other_element]) ** 2)
                * alloy.composition[element]
                * alloy.composition[other_element]
            )

            y_2 += (
                diameters[element]
                * diameters[other_element]
                * ((diameters[element] - diameters[other_element]) ** 2)
                * alloy.composition[element]
                * alloy.composition[other_element]
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


def mixing_entropy(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the mixing entropy of an alloy, combining the
    :func:`~metallurgy.entropy.ideal_entropy` and
    :func:`~metallurgy.entropy.mismatch_entropy`.

    :group: calculations.entropy

    Parameters
    ----------

    alloy
        The alloy for which to calculate the mixing entropy.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_entropy(a) for a in alloy]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    ideal = ideal_entropy(alloy)
    mismatch = mismatch_entropy(alloy)

    if ideal is not None and mismatch is not None:
        return ideal + mismatch

    return None
