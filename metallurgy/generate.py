import re
from typing import Union, Optional, List

import numpy as np
import elementy

import metallurgy as mg


def random_alloy(
    min_elements: int = 1,
    max_elements: int = 10,
    percentage_constraints={},
    allowed_elements=[e for e in elementy.PeriodicTable().elements],
):
    """Generate a random alloy.

    :group: alloy.generate

    Parameters
    ----------

    min_elements
        Minimum number of elements in the random alloy.

    """

    if isinstance(percentage_constraints, (list)):
        parsed_percentage_constraints = {}
        for element in percentage_constraints:
            parsed_percentage_constraints[element] = {}
        percentage_constraints = parsed_percentage_constraints

    if min_elements < max_elements:
        num_extra_elements = np.random.randint(min_elements, max_elements + 1)
    else:
        num_extra_elements = max_elements
    num_extra_elements -= len(percentage_constraints)

    if num_extra_elements > 0:
        other_elements = allowed_elements[:]
        for element in percentage_constraints:
            if element in other_elements:
                other_elements.remove(element)

        elements = list(percentage_constraints.keys()) + list(
            np.random.choice(
                other_elements,
                min(num_extra_elements, len(other_elements)),
                replace=False,
            )
        )

    else:
        elements = list(
            np.random.choice(
                list(percentage_constraints.keys()),
                num_extra_elements + len(percentage_constraints.keys()),
                replace=False,
            )
        )

    percentages = list(np.random.dirichlet(np.ones(len(elements)), size=1)[0])

    composition = {}
    for j in range(len(elements)):
        composition[elements[j]] = percentages[j]

    alloy = mg.Alloy(
        composition,
        constraints={
            "percentages": percentage_constraints,
            "min_elements": min_elements,
            "max_elements": max_elements,
        },
    )

    return alloy


def random_alloys(
    num_alloys: int,
    min_elements: int = 1,
    max_elements: int = 10,
    percentage_constraints: dict = {},
    allowed_elements: list = [e for e in elementy.PeriodicTable().elements],
):
    """Generate multiple random alloys.

    :group: alloy.generate

    Parameters
    ----------

    min_elements
        Minimum number of elements in the random alloy.

    """

    return [
        random_alloy(
            min_elements,
            max_elements,
            percentage_constraints,
            allowed_elements,
        )
        for _ in range(num_alloys)
    ]


def mixture(alloys: List[mg.Alloy], weights: Optional[list] = None):
    """Mix some alloys.

    :group: alloy.generate

    Parameters
    ----------

    alloys
        The alloys to be mixed.
    weights
        The weighting applied to the mixing of alloys.

    """

    shared_composition_space = []
    for alloy in alloys:
        for element in alloy.elements:
            if element not in shared_composition_space:
                shared_composition_space.append(element)

    constraints = None
    for alloy in alloys:
        if alloy.constraints is not None:
            if constraints is None:
                constraints = {
                    "percentages": {},
                    "min_elements": 1,
                    "max_elements": 1,
                }

            if "min_elements" in alloy.constraints:
                constraints["min_elements"] = max(
                    constraints["min_elements"],
                    alloy.constraints["min_elements"],
                )
            if "max_elements" in alloy.constraints:
                constraints["max_elements"] = max(
                    constraints["max_elements"],
                    alloy.constraints["max_elements"],
                )

            if "percentages" in alloy.constraints:
                for element in alloy.constraints["percentages"]:
                    if element not in constraints:
                        constraints["percentages"][element] = {}

                    if "min" in alloy.constraints["percentages"][element]:
                        if "min" not in constraints["percentages"][element]:
                            constraints["percentages"][element][
                                "min"
                            ] = alloy.constraints["percentages"][element][
                                "min"
                            ]
                        else:
                            constraints["percentages"][element]["min"] = min(
                                constraints["percentages"][element]["min"],
                                alloy.constraints["percentages"][element][
                                    "min"
                                ],
                            )

                    if "max" in alloy.constraints["percentages"][element]:
                        if "max" not in constraints["percentages"][element]:
                            constraints["percentages"][element][
                                "max"
                            ] = alloy.constraints["percentages"][element][
                                "max"
                            ]
                        else:
                            constraints["percentages"][element]["max"] = max(
                                constraints["percentages"][element]["max"],
                                alloy.constraints["percentages"][element][
                                    "max"
                                ],
                            )

    if weights is None:
        weights = [1.0] * len(alloys)

    mixed_composition = {}
    for element in shared_composition_space:
        mixed_composition[element] = 0
        for i in range(len(alloys)):
            if element in alloys[i].elements:
                mixed_composition[element] += (
                    alloys[i].composition[element] * weights[i]
                )

    return mg.Alloy(mixed_composition, constraints=constraints)


def system(
    elements: Union[list, str],
    step: Union[int, float] = 1,
    min_percent: Union[int, float] = 0,
    max_percent: Union[int, float] = 100,
    property_name: Optional[str] = None,
):
    """Generate a set of alloys in a particular elemental composition-space.

    :group: alloy.generate

    Parameters
    ----------

    elements
        The elements of the composition-space.
    step
        The percentage step between alloys in the composition-space.
    min_percent
        The minimum percentage of each element in alloys in the composition-space.
    max_percent
        The maximum percentage of each element in alloys in the
        composition-space.
    property_name
        A property to calculate for all alloys in the set generated.

    """

    if isinstance(elements, str):
        elements = re.findall("[A-Z][^A-Z]*", elements)

    if len(elements) == 2:
        return binary(elements, step, property_name)
    elif len(elements) == 3:
        return ternary(
            elements, step, min_percent, max_percent, property_name, quaternary
        )


def binary(
    elements: Union[list, str],
    step: Union[int, float] = 0.5,
    property_name: Optional[str] = None,
):
    """Generate a set of binary alloys in a particular elemental composition-space.

    :group: alloy.generate

    Parameters
    ----------

    elements
        The elements of the composition-space.
    step
        The percentage step between alloys in the composition-space.
    property_name
        A property to calculate for all alloys in the set generated.

    """

    if isinstance(elements, str):
        elements = re.findall("[A-Z][^A-Z]*", elements)

    x = 100
    alloys = []
    percentages = []
    while x >= 0:
        alloys.append(
            mg.Alloy(
                elements[0] + str(x) + elements[1] + str(100 - x),
                rescale=False,
            )
        )
        percentages.append(x)
        x -= step

    if property_name is not None:
        values = mg.calculate(alloys, property_name)
        return alloys, percentages, values

    return alloys, percentages


def ternary(
    elements: Union[list, str],
    step: Union[int, float] = 1,
    min_percent: Union[int, float] = 0,
    max_percent: Union[int, float] = 100,
    property_name: Optional[str] = None,
    quaternary: Optional[dict] = None,
):
    """Generate a set of ternary alloys.

    :group: alloy.generate

    Parameters
    ----------

    elements
        The elements of the composition-space.
    step
        The percentage step between alloys in the composition-space.
    min_percent
        The minimum percentage of each element in alloys in the composition-space.
    max_percent
        The maximum percentage of each element in alloys in the
        composition-space.
    property_name
        A property to calculate for all alloys in the set generated.
    quaternary
        True if this ternary system is a member of an encompassing quaternary system.

    """

    if isinstance(elements, str):
        elements = re.findall("[A-Z][^A-Z]*", elements)

    alloys = []
    percentages = []

    tmp_percentages = [max_percent + step] * 3
    while tmp_percentages[0] >= min_percent + step:
        tmp_percentages[0] -= step
        tmp_percentages[1] = max_percent + step
        tmp_percentages[2] = max_percent + step

        while tmp_percentages[1] >= min_percent + step:
            tmp_percentages[1] -= step
            tmp_percentages[2] = max_percent + step

            while tmp_percentages[2] >= min_percent + step:
                tmp_percentages[2] -= step

                if sum(tmp_percentages) == 100:

                    composition_str = ""
                    for i in range(len(elements)):
                        if tmp_percentages[i] > 0:
                            composition_str += elements[i] + str(
                                tmp_percentages[i]
                            )

                    if quaternary is not None:
                        composition_str = (
                            "("
                            + composition_str
                            + ")"
                            + str(100 - quaternary[1])
                            + quaternary[0]
                            + str(quaternary[1])
                        )

                    alloy = mg.Alloy(composition_str, rescale=False)

                    alloys.append(alloy)
                    percentages.append(list(alloy.composition.values()))

    if property_name is not None:
        values = mg.calculate(alloys, property_name)
        return alloys, percentages, values

    return alloys, percentages
