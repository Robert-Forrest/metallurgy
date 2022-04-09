from collections.abc import Iterable

import metallurgy as mg
from . import linear_mixture
from .alloy import Alloy


def price(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [price(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    total_weight = linear_mixture(alloy, 'mass')

    price = 0
    for element in alloy.elements:
        weight_percent = mg.periodic_table.elements[element]['mass'] * \
            alloy.composition[element] / total_weight
        price += weight_percent * mg.periodic_table.elements[element]['price']

    return price
