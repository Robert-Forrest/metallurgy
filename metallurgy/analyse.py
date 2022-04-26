import re

import numpy as np

from . import generate


def find_max(elements, feature_name):
    if isinstance(elements, str):
        elements = re.findall('[A-Z][^A-Z]*', elements)

    system = generate.system(elements, feature_name=feature_name)
    if system is not None:

        alloys, percentages, values = system

        max_index = np.argmax(values)

        return alloys[max_index], values[max_index]


def find_min(elements, feature_name):
    if isinstance(elements, str):
        elements = re.findall('[A-Z][^A-Z]*', elements)

    system = generate.system(elements, feature_name=feature_name)
    if system is not None:

        alloys, percentages, values = system

        min_index = np.argmin(values)

        return alloys[min_index], values[min_index]
