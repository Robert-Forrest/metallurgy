"""
``metallurgy.linear_mixture``
=============================

Module enabling calculation of linear mixtures of
elemental properties, as an approximation to the
properties of an alloy.
"""

from numbers import Number
from collections.abc import Iterable

import metallurgy as mg
from .alloy import Alloy


def linear_mixture(alloy, property_name) -> Number:
    """Returns the linear mixture of a particular elemental property of an
    alloy.

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the linear mixture.
    property_name : str
        The elemental property to calcualate the linear mixture of.
    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [linear_mixture(a, property_name) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    mixed_property = 0
    for element in alloy.elements:
        value = mg.periodic_table.elements[element][property_name]
        if value is None:
            return None
        elif isinstance(value, list):
            value = value[0]

        if not isinstance(value, Number):
            return None

        mixed_property += alloy.composition[element] * value

    return mixed_property
