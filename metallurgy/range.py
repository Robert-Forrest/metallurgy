"""``metallurgy.range``
=============================

Module enabling calculation of linear mixtures of elemental properties, as an
approximation to the properties of an alloy.

"""

from typing import Union, List
from numbers import Number
from collections.abc import Iterable

import numpy as np

import metallurgy as mg


def range(
    alloy: Union[mg.Alloy, str, dict], property_name: str
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the range of a particular elemental property of an
    alloy.

    :group: calculations

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the linear mixture.
    property_name : str
        The elemental property to calcualate the linear mixture of.

    """

    # If a list of alloys is given, return a list of linear mixture data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [range(a, property_name) for a in list(alloy)]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    # Calculate the range
    per_element_values = []
    for element in alloy.elements:
        # Get the current element's value of the property from elementy
        value = mg.periodic_table.elements[element][property_name]

        # Return None if no data for the element
        if value is None:
            return None
        # Use the first entry for the property if multiple
        elif isinstance(value, list):
            value = value[0]

        # If not numerical data, return None
        if not isinstance(value, Number):
            return None

        # Element's contribution to the linear mixture, weighted by composition
        per_element_values.append(alloy.composition[element] * value)

    return np.abs(np.max(per_element_values) - np.min(per_element_values))
