"""Module enabling calculation of radius related alloy properties."""

from typing import Union, List
from collections.abc import Iterable

import numpy as np

import metallurgy as mg


def radius_gamma(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[float, None, List[Union[float, None]]]:
    """Returns the radius gamma property for an alloy.

    :group: calculations.radii

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the linear mixture.

    """

    # If a list of alloys is given, return a list of data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [radius_gamma(a) for a in alloy]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    max_radius = 0
    min_radius = 1000

    mean_radius = 0
    for element in alloy.elements:
        mean_radius += (
            alloy.composition[element]
            * mg.periodic_table.elements[element]["radius"]
        )

    for element in alloy.elements:
        r = mg.periodic_table.elements[element]["radius"]
        if r > max_radius:
            max_radius = r
        if r < min_radius:
            min_radius = r

    r_min_delta_sq = (min_radius + mean_radius) ** 2
    r_max_delta_sq = (max_radius + mean_radius) ** 2
    r_mean_sq = mean_radius**2

    numerator = 1.0 - np.sqrt((r_min_delta_sq - r_mean_sq) / (r_min_delta_sq))
    denominator = 1.0 - np.sqrt(
        (r_max_delta_sq - r_mean_sq) / (r_max_delta_sq)
    )

    return numerator / denominator


def lattice_distortion(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[float, None, List[Union[float, None]]]:
    """Returns the lattice distortion of an alloy.

    :group: calculations.radii

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the linear mixture.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [lattice_distortion(a) for a in alloy]
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    mean_radius = 0
    for element in alloy.elements:
        radius = mg.periodic_table.elements[element]["radius"]
        if radius is None:
            return None

        mean_radius += alloy.composition[element] * radius

    _lattice_distortion = 0
    for i in range(len(alloy.elements) - 1):
        for j in range(i + 1, len(alloy.elements)):
            element = alloy.elements[i]
            other_element = alloy.elements[j]

            radius_a = (
                alloy.composition[element]
                * mg.periodic_table.elements[element]["radius"]
            )
            radius_b = (
                alloy.composition[element]
                * mg.periodic_table.elements[other_element]["radius"]
            )

            _lattice_distortion += (
                alloy.composition[element]
                * alloy.composition[other_element]
                * np.abs(radius_a + radius_b - 2 * mean_radius)
            ) / (2 * mean_radius)

    return _lattice_distortion
