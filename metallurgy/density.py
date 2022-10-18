"""``metallurgy.density``
=============================

Module providing density related calculations.

"""

from typing import Union, List
from collections.abc import Iterable

import metallurgy as mg


def theoretical_density(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[float, None, List[Union[float, None]]]:
    """Returns the theoretical density of an alloy.

    :group: calculations.density

    Parameters
    ----------

    alloy : mg.Alloy, str, dict
        The alloy for which to calculate the theoretcial density.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [theoretical_density(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    massFractions = {}
    masses = {}
    totalMass = 0
    for element in alloy.elements:
        masses[element] = mg.periodic_table.elements[element]["mass"]
        totalMass += masses[element] * alloy.composition[element]

    for element in alloy.elements:
        massFractions[element] = (
            alloy.composition[element] * masses[element] / totalMass
        )

    total = 0
    for element in alloy.elements:
        total += (
            massFractions[element]
            / mg.periodic_table.elements[element]["density"]
        )

    return 1 / total
