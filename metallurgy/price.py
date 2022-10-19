"""``metallurgy.price``
=============================

Module enabling calculation of approximate alloy price.

"""

from typing import Union, List
from collections.abc import Iterable

import metallurgy as mg


def price(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[float, None, List[Union[float, None]]]:
    """Returns the approximate price per kilogramme of an alloy.

    :group: calculations.price

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the linear mixture.

    """

    # If a list of alloys is given, return a list of price data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [price(a) for a in alloy]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    # Get the total mass to enable conversion of atomic percent to weight percent
    total_mass = mg.linear_mixture(alloy, "mass")

    total_price = 0
    for element in alloy.elements:
        # Only attempt calculation if pricing data is available
        if mg.periodic_table.elements[element]["price"] is not None:
            # Convert atomic percent to weight percent
            weight_percent = (
                mg.periodic_table.elements[element]["mass"]
                * alloy.composition[element]
                / total_mass
            )

            # Add weighted contribution to the price approximation
            total_price += (
                weight_percent * mg.periodic_table.elements[element]["price"]
            )
        else:
            return None

    return total_price
