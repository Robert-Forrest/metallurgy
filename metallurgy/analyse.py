"""Module enabling analysis of alloy data"""

import re
from typing import Tuple, Union
from numbers import Number

import numpy as np

import metallurgy as mg


def find_max(
    elements: list[str], property_name: str
) -> Union[Tuple[mg.Alloy, Number], None]:
    """Finds the maximum value of a property in an alloy system.

    :group: alloy.generate

    Parameters
    ----------

    elements
        The elements of the alloy system.
    property_name
        The property to find the maximum of.

    """

    if isinstance(elements, str):
        elements = re.findall("[A-Z][^A-Z]*", elements)

    system = mg.generate.system(elements, property_name=property_name)
    if system is not None:

        alloys, percentages, values = system

        max_index = np.argmax(values)

        return alloys[max_index], values[max_index]


def find_min(
    elements: list[str], property_name: str
) -> Union[Tuple[mg.Alloy, Number], None]:
    """Finds the minimum value of a property in an alloy system.

    :group: alloy.generate

    Parameters
    ----------

    elements
        The elements of the alloy system.
    property_name
        The property to find the minimum of.

    """

    if isinstance(elements, str):
        elements = re.findall("[A-Z][^A-Z]*", elements)

    system = mg.generate.system(elements, property_name=property_name)
    if system is not None:

        alloys, percentages, values = system

        min_index = np.argmin(values)

        return alloys[min_index], values[min_index]
