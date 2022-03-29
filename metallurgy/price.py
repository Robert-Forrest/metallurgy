import metallurgy as mg
from . import linear_mixture
from .alloy import Alloy


def calculate_price(alloy):
    if not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    total_weight = linear_mixture(alloy, 'mass')

    price = 0
    for element in alloy.elements:
        weight_percent = mg.periodic_table.dict[element]['mass'] * \
            alloy.composition[element] / total_weight
        price += weight_percent * mg.periodic_table.dict[element]['price']

    return price
