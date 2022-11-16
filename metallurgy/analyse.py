"""Module enabling analysis of alloy data"""

import re
from typing import Tuple, Union, List
from numbers import Number

import numpy as np

import metallurgy as mg


def find_max(
    elements: List[str], property_name: str
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
    elements: List[str], property_name: str
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


def find_unique_elements(alloys: List[mg.Alloy]) -> List[str]:
    """Finds the unique elements in a list of alloy compositions.

    :group: alloy.utils

    Parameters
    ----------

    alloys
        List of alloys in which to find the unique elements.

    """

    unique_elements = []
    for alloy in alloys:
        for element in alloy.elements:
            if element not in unique_elements:
                unique_elements.append(element)

    return unique_elements


def find_unique_percentages(alloys: List[mg.Alloy]) -> dict:
    """Finds the unique percentages per element in a list of alloy compositions.

    :group: alloy.utils

    Parameters
    ----------

    alloys
        List of alloys in which to find the unique percentages.

    """

    unique_elements = find_unique_elements(alloys)
    percentages = {e: [] for e in unique_elements}
    for alloy in alloys:
        for element in alloy.composition:
            percentage = alloy.composition[element]
            if percentage not in percentages[element]:
                percentages[element].append(percentage)

    return percentages


def composition_weighted_average(alloys, data):
    unique_elements = find_unique_elements(alloys)

    per_element_property = {e: 0 for e in unique_elements}
    per_element_total = {e: 0 for e in unique_elements}
    for i, alloy in enumerate(alloys):
        for element in alloy.composition:
            if data[i] is None:
                continue

            per_element_property[element] += (
                data[i] * alloy.composition[element]
            )
            per_element_total[element] += alloy.composition[element]

    for element in per_element_property:
        if per_element_total[element] > 0:
            per_element_property[element] /= per_element_total[element]
        else:
            per_element_property[element] = None

    return per_element_property
