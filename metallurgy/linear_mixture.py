import numbers
from collections.abc import Iterable

import metallurgy as mg
from .alloy import Alloy


def linear_mixture(alloy, feature_name):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [linear_mixture(a, feature_name) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    mixed_property = 0
    for element in alloy.elements:
        value = mg.periodic_table.elements[element][feature_name]
        if value is None:
            return None
        elif isinstance(value, list):
            value = value[0]

        if not isinstance(value, numbers.Number):
            return None

        mixed_property += alloy.composition[element] * value

    return mixed_property
