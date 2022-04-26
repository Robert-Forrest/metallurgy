import re
from typing import Union, Optional

import numpy as np
import elementy

from .alloy import Alloy
from .calculate import calculate


def random_alloy(
        min_elements: int = 1,
        max_elements: int = 10,
        percentage_constraints={},
        allowed_elements=[e for e in elementy.PeriodicTable().elements]):

    if isinstance(percentage_constraints, (list)):
        parsed_percentage_constraints = {}
        for element in percentage_constraints:
            parsed_percentage_constraints[element] = {}
        percentage_constraints = parsed_percentage_constraints

    if min_elements < max_elements:
        num_extra_elements = np.random.randint(
            min_elements, max_elements)
    else:
        num_extra_elements = max_elements
    num_extra_elements -= len(percentage_constraints)

    if num_extra_elements > 0:
        other_elements = allowed_elements[:]
        for element in percentage_constraints:
            if element in other_elements:
                other_elements.remove(element)
        elements = list(percentage_constraints.keys()) + \
            list(np.random.choice(other_elements, num_extra_elements, replace=False))

    else:
        elements = list(np.random.choice(
            list(percentage_constraints.keys()),
            num_extra_elements + len(percentage_constraints.keys()),
            replace=False))

    percentages = list(np.random.dirichlet(np.ones(len(elements)), size=1)[0])

    composition = {}
    for j in range(len(elements)):
        composition[elements[j]] = percentages[j]

    alloy = Alloy(
        composition,
        {
            'percentages': percentage_constraints,
            'min_elements': min_elements,
            'max_elements': max_elements
        }
    )

    alloy.rescale()

    return alloy


def random_alloys(num_alloys: int,
                  min_elements: int = 1,
                  max_elements: int = 10,
                  percentage_constraints: dict = {},
                  allowed_elements: list = [e for e in elementy.PeriodicTable().elements]):

    return [
        random_alloy(
            min_elements,
            max_elements,
            percentage_constraints,
            allowed_elements
        ) for _ in range(num_alloys)]


def mixture(alloys, weights: Optional[list] = None):
    shared_composition_space = []

    for alloy in alloys:
        for element in alloy.elements:
            if element not in shared_composition_space:
                shared_composition_space.append(element)

    if weights is None:
        weights = [1.0]*len(alloys)

    mixed_composition = {}
    for element in shared_composition_space:
        mixed_composition[element] = 0
        for i in range(len(alloys)):
            if element in alloys[i].elements:
                mixed_composition[element] += alloys[i].composition[element]*weights[i]

    return Alloy(mixed_composition)


def system(
        elements: Union[list, str],
        step: Union[int, float] = 1,
        min_percent: Union[int, float] = 0,
        max_percent: Union[int, float] = 100,
        feature_name: Optional[str] = None,
        quaternary: Optional[dict] = None):

    if isinstance(elements, str):
        elements = re.findall('[A-Z][^A-Z]*', elements)

    if len(elements) == 2:
        return binary(elements, step, feature_name)
    elif len(elements) == 3:
        return ternary(elements, step, min_percent, max_percent, feature_name, quaternary)


def binary(
        elements: Union[list, str],
        step: Union[int, float] = 0.5,
        feature_name: Optional[str] = None):

    if isinstance(elements, str):
        elements = re.findall('[A-Z][^A-Z]*', elements)

    x = 100
    alloys = []
    percentages = []
    while x >= 0:
        alloys.append(Alloy(
            elements[0] + str(x) + elements[1] + str(100 - x), rescale=False))
        percentages.append(x)
        x -= step

    if feature_name is not None:
        values = calculate(alloys, feature_name)
        return alloys, percentages, values

    return alloys, percentages


def ternary(
        elements: Union[list, str],
        step: Union[int, float] = 1,
        min_percent: Union[int, float] = 0,
        max_percent: Union[int, float] = 100,
        feature_name: Optional[str] = None,
        quaternary: Optional[dict] = None):

    if isinstance(elements, str):
        elements = re.findall('[A-Z][^A-Z]*', elements)

    alloys = []
    percentages = []

    tmp_percentages = [max_percent+step]*3
    while tmp_percentages[0] >= min_percent+step:
        tmp_percentages[0] -= step
        tmp_percentages[1] = max_percent+step
        tmp_percentages[2] = max_percent+step

        while tmp_percentages[1] >= min_percent+step:
            tmp_percentages[1] -= step
            tmp_percentages[2] = max_percent + step

            while tmp_percentages[2] >= min_percent+step:
                tmp_percentages[2] -= step

                if(sum(tmp_percentages) == 100):

                    composition_str = ""
                    for i in range(len(elements)):
                        if(tmp_percentages[i] > 0):
                            composition_str += elements[i] + \
                                str(tmp_percentages[i])

                    if quaternary is not None:
                        composition_str = "(" + composition_str + ")" + str(
                            100 - quaternary[1]) + quaternary[0] + str(quaternary[1])

                    alloy = Alloy(composition_str, rescale=False)

                    alloys.append(alloy)
                    percentages.append(list(alloy.composition.values()))

    if feature_name is not None:
        values = calculate(alloys, feature_name)
        return alloys, percentages, values

    return alloys, percentages
