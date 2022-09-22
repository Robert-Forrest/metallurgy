from collections.abc import Iterable

import metallurgy as mg
from . import linear_mixture
from .alloy import Alloy


def price(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [price(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    total_weight = linear_mixture(alloy, "mass")

    total_price = 0
    for element in alloy.elements:
        if mg.periodic_table.elements[element]["price"] is not None:
            weight_percent = (
                mg.periodic_table.elements[element]["mass"]
                * alloy.composition[element]
                / total_weight
            )
            total_price += (
                weight_percent * mg.periodic_table.elements[element]["price"]
            )
        else:
            return None

    return total_price
