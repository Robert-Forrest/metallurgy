"""``metallurgy.analyse``
=============================

Module enabling analysis of alloy data

"""

import re
from typing import Tuple, Union
from numbers import Number

import numpy as np

from . import generate
from .alloy import Alloy


def find_max(
    elements: list[str], property_name: str
) -> Union[Tuple[Alloy, Number], None]:
    if isinstance(elements, str):
        elements = re.findall("[A-Z][^A-Z]*", elements)

    system = generate.system(elements, property_name=property_name)
    if system is not None:

        alloys, percentages, values = system

        max_index = np.argmax(values)

        return alloys[max_index], values[max_index]


def find_min(
    elements: list[str], property_name: str
) -> Union[Tuple[Alloy, Number], None]:
    if isinstance(elements, str):
        elements = re.findall("[A-Z][^A-Z]*", elements)

    system = generate.system(elements, property_name=property_name)
    if system is not None:

        alloys, percentages, values = system

        min_index = np.argmin(values)

        return alloys[min_index], values[min_index]
