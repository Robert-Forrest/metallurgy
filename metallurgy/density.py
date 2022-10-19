"""Module providing density related calculations."""

from typing import Union, List
from collections.abc import Iterable
from numbers import Number

import metallurgy as mg


def theoretical_density(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the theoretical density of an alloy.  See equation 8 of
    https://doi.org/10.1016/j.jnoncrysol.2019.03.001.

    :group: calculations.density

    Parameters
    ----------

    alloy
        The alloy for which to calculate the theoretcial density.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [theoretical_density(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    mass_fractions = {}
    masses = {}
    total_mass = 0
    for element in alloy.elements:
        masses[element] = mg.periodic_table.elements[element]["mass"]
        total_mass += masses[element] * alloy.composition[element]

    for element in alloy.elements:
        mass_fractions[element] = (
            alloy.composition[element] * masses[element] / total_mass
        )

    total = 0
    for element in alloy.elements:
        total += (
            mass_fractions[element]
            / mg.periodic_table.elements[element]["density"]
        )

    return 1 / total
