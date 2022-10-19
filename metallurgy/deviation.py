"""Module enabling calculation of deviations of elemental properties in alloys."""


from typing import Union, List
from numbers import Number
from collections.abc import Iterable

import numpy as np
import metallurgy as mg


def deviation(
    alloy: Union[mg.Alloy, str, dict], property_name: str
) -> Union[float, None, List[Union[float, None]]]:
    """Returns the deviation of a particular elemental property in an
    alloy.

    See equation 6 of the paper "Machine-learning improves understanding of
    glass formation in metallic systems" for definition of the deviation:
    https://pubs.rsc.org/en/content/articlelanding/2022/dd/d2dd00026a

    :group: calculations

    Parameters
    ----------

    alloy
        The alloy for which to calculate the linear mixture.
    property_name
        The elemental property to calcualate the linear mixture of.

    """

    # If a list of alloys is given, return a list of deviation data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [deviation(a, property_name) for a in list(alloy)]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    # Deviation only makes sense for multi-element alloys
    if len(alloy.elements) > 1:

        # If property is numerical, calculate the deviation of the values
        if isinstance(
            mg.periodic_table.elements[alloy.elements[0]][property_name],
            (Number, list),
        ):

            # Calculate the mean value of the property in the alloy
            mean = 0
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][property_name]

                # Return None if property is None
                if value is None:
                    return None

                # Take first entry if property is a list
                if isinstance(value, list):
                    value = value[0]

                # Return None if property is not numerical
                if not isinstance(value, Number):
                    return None

                mean += alloy.composition[element] * value

            # Calculate the deviation of the property in the alloy
            total_deviation = 0
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][property_name]

                # Return None if property is None
                if value is None:
                    return None

                # Take first entry if property is a list
                if isinstance(value, list):
                    value = value[0]

                # Return None if property is not numerical
                if not isinstance(value, Number):
                    return None

                total_deviation += alloy.composition[element] * (
                    (value - mean) ** 2
                )

            return total_deviation**0.5

        # If property is non-numerical, calculate the shannon entropy of the
        # values
        else:

            # Count unique values of the property
            value_count = {}
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][property_name]
                if value is None:
                    return None

                if value not in value_count:
                    value_count[value] = 0
                value_count[value] += alloy.composition[element]

            # Shannon entropy is only non-zero if multiple unique values
            if len(value_count) > 1:
                shannonEntropy = 0
                for value in value_count:
                    shannonEntropy -= value_count[value] * np.log(
                        value_count[value]
                    )
                return shannonEntropy
            else:
                return 0.0

    # Single element alloys have zero deviation
    else:
        return 0.0
