import re
from numbers import Number
from typing import List, Optional, Union

import elementy
import numpy as np

import metallurgy as mg

from .prototypes import get_random_prototype


def random_alloy(
    min_elements: int = 1,
    max_elements: int = 10,
    percentage_constraints: Optional[dict] = None,
    percentage_step: Optional[float] = None,
    allowed_elements: Optional[list] = None,
    constrain_alloy: bool = False,
    structure: bool = False,
):
    """Generate a random alloy.

    :group: alloy.generate

    Parameters
    ----------

    min_elements
        Minimum number of elements in the random alloy.

    """

    if allowed_elements is None:
        allowed_elements = [e for e in elementy.PeriodicTable().elements]
    if percentage_step is None:
        percentage_step = 0.01

    if percentage_constraints is None:
        percentage_constraints = {}
    if isinstance(percentage_constraints, (list)):
        parsed_percentage_constraints = {}
        for element in percentage_constraints:
            parsed_percentage_constraints[element] = {}
        percentage_constraints = parsed_percentage_constraints

    if min_elements < max_elements:
        num_extra_elements = np.random.randint(min_elements, max_elements + 1)
    else:
        num_extra_elements = max_elements

    constrained_elements = list(percentage_constraints.keys())
    if "*" in constrained_elements:
        constrained_elements.remove("*")
    num_constrained_elements = len(constrained_elements)
    num_extra_elements -= num_constrained_elements

    if num_extra_elements > 0:
        other_elements = allowed_elements[:]
        for element in percentage_constraints:
            if element in other_elements:
                other_elements.remove(element)

        elements = constrained_elements + list(
            np.random.choice(
                other_elements,
                min(num_extra_elements, len(other_elements)),
                replace=False,
            )
        )

    elif max_elements == min_elements:
        if max_elements == num_constrained_elements:
            elements = constrained_elements
        elif max_elements == len(allowed_elements):
            elements = allowed_elements[:]
        else:
            elements = list(
                np.random.choice(
                    allowed_elements,
                    max_elements,
                    replace=False,
                )
            )

    else:
        elements = list(
            np.random.choice(
                constrained_elements,
                num_extra_elements + num_constrained_elements,
                replace=False,
            )
        )

    if not structure:
        percentages = np.random.rand(len(elements))
        percentages = (
            percentages
            / percentages.sum()
            * (1 - percentage_step * len(elements))
        )
        percentages += percentage_step

        composition = {}
        for j in range(len(elements)):
            composition[elements[j]] = percentages[j]
    else:
        composition = "".join(elements)
        if isinstance(structure, bool):
            composition += "[" + get_random_prototype().name + "]"
        else:
            composition += "[" + get_random_prototype(structure).name + "]"

    alloy = mg.Alloy(
        composition,
        constraints={
            "percentages": percentage_constraints,
            "percentage_step": percentage_step,
            "min_elements": min_elements,
            "max_elements": max_elements,
            "allowed_elements": allowed_elements,
        },
    )

    if not constrain_alloy:
        alloy.constraints = None
    else:
        alloy.rescale()

    return alloy


def random_alloys(
    num_alloys: int,
    min_elements: int = 1,
    max_elements: int = 10,
    percentage_constraints: Optional[dict] = None,
    percentage_step=0.01,
    allowed_elements: list = [e for e in elementy.PeriodicTable().elements],
    constrain_alloys=False,
    structures=False,
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
            percentage_step,
            allowed_elements,
            constrain_alloy=constrain_alloys,
            structure=structures,
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

    for i in range(len(alloys)):
        if not isinstance(alloys[i], mg.Alloy):
            alloys[i] = mg.Alloy(alloys[i])

    if len(alloys) == 1:
        return alloys[0]

    shared_composition_space = []
    structures = []
    for alloy in alloys:
        for element in alloy.elements:
            if element not in shared_composition_space:
                shared_composition_space.append(element)
        structures.append(alloy.structure)

    constraints = None
    for alloy in alloys:
        if alloy.constraints is not None:
            if constraints is None:
                constraints = {
                    "percentages": {},
                    "min_elements": 1,
                    "max_elements": 1,
                    "percentage_step": 0.01,
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
            if "percentage_step" in alloy.constraints:
                constraints["percentage_step"] = min(
                    constraints["percentage_step"],
                    alloy.constraints["percentage_step"],
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

                    if (
                        "precedence"
                        in alloy.constraints["percentages"][element]
                    ):
                        if (
                            "precedence"
                            not in constraints["percentages"][element]
                        ):
                            constraints["percentages"][element][
                                "precedence"
                            ] = alloy.constraints["percentages"][element][
                                "precedence"
                            ]
                        else:
                            constraints["percentages"][element][
                                "precedence"
                            ] = max(
                                constraints["percentages"][element][
                                    "precedence"
                                ],
                                alloy.constraints["percentages"][element][
                                    "precedence"
                                ],
                            )

    if weights is None:
        weights = [1.0 / len(alloys)] * len(alloys)

    mixed_composition = {}
    for element in shared_composition_space:
        mixed_composition[element] = 0
        for i in range(len(alloys)):
            if element in alloys[i].elements:
                mixed_composition[element] += (
                    alloys[i].composition[element] * weights[i]
                )

    structure = [
        s
        for _, s in sorted(zip(weights, structures), key=lambda pair: pair[0])
    ][0]

    return mg.Alloy(
        mixed_composition, structure=structure, constraints=constraints
    )


def system(
    elements: Union[list, str],
    step: Number = 1,
    min_percent: Number = 0,
    max_percent: Number = 100,
    property_name: Optional[str] = None,
    crystal_structure: Optional[str] = None,
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
        return binary(
            elements, step, property_name, crystal_structure=crystal_structure
        )
    elif len(elements) == 3:
        return ternary(
            elements,
            step,
            min_percent,
            max_percent,
            property_name,
            crystal_structure=crystal_structure,
        )
    elif len(elements) == 4:
        return quaternary(
            elements,
            step,
            min_percent,
            max_percent,
            property_name,
            crystal_structure=crystal_structure,
        )


def binary(
    elements: Union[list, str],
    step: Number = 0.5,
    property_name: Optional[str] = None,
    crystal_structure: Optional[str] = None,
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
    if len(elements) != 2:
        raise ValueError("Binary system must have 2 elements")

    x = 100
    alloys = []
    percentages = []
    while x >= 0:
        alloy_str = elements[0] + str(x) + elements[1] + str(100 - x)
        if crystal_structure is not None:
            alloy_str += "[" + crystal_structure + "]"
        alloys.append(mg.Alloy(alloy_str))
        percentages.append(x)
        x -= step

    if property_name is not None:
        values = mg.calculate(alloys, property_name)
        return alloys, percentages, values

    return alloys, percentages


def ternary(
    elements: Union[list, str],
    step: Number = 1,
    min_percent: Number = 0,
    max_percent: Number = 100,
    property_name: Optional[str] = None,
    quaternary_element: Optional[tuple] = None,
    crystal_structure: Optional[str] = None,
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
    quaternary_element
        If this ternary system is a member of an encompassing quaternary system
        provide the quaternary element and its percentage.

    """

    if isinstance(elements, str):
        elements = re.findall("[A-Z][^A-Z]*", elements)
    if len(elements) != 3:
        raise ValueError("Ternary system must have 3 elements")

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

                    if quaternary_element is not None:
                        composition_str = (
                            "("
                            + composition_str
                            + ")"
                            + str(100 - quaternary_element[1])
                            + quaternary_element[0]
                            + str(quaternary_element[1])
                        )

                    if crystal_structure is not None:
                        composition_str += "[" + crystal_structure + "]"

                    alloy = mg.Alloy(composition_str)
                    alloys.append(alloy)
                    percentages.append(list(alloy.composition.values()))

    if property_name is not None:
        values = mg.calculate(alloys, property_name)
        return alloys, percentages, values

    return alloys, percentages


def quaternary(
    elements: Union[list, str],
    step: Number = 1,
    min_percent: Number = 0,
    max_percent: Number = 100,
    min_quaternary_percent: Number = 0,
    quaternary_percent_step: Number = 25,
    quaternary_percentages: Optional[List[Number]] = None,
    property_name: Optional[str] = None,
    crystal_structure: Optional[str] = None,
):
    """Generate a set of quaternary alloys.

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
    if len(elements) != 4:
        raise ValueError("Quaternary system must have 4 elements")

    alloys = []

    if quaternary_percentages is None:
        quaternary_percentages = []
        quaternary_percentage = 0
        quaternary_step = 25
        while quaternary_percentage < 100:
            quaternary_percentages.append(quaternary_percentage)
            quaternary_percentage += quaternary_step

    for quaternary_percentage in quaternary_percentages:
        ternary_alloys, ternary_percentages = ternary(
            elements[:3],
            quaternary_element=(elements[3], quaternary_percentage),
            crystal_structure=crystal_structure,
        )
        alloys.append(ternary_alloys)

    return alloys


def perturb(alloy, size=0.05):
    if isinstance(alloy, list):
        return [perturb(a) for a in alloy]

    composition = dict(alloy.composition)
    structure = alloy.structure
    constraints = alloy.constraints
    if "local_percentages" in constraints:
        del constraints["local_percentages"]
    if "digits" in constraints:
        del constraints["digits"]

    for element in composition:
        composition[element] += round(
            float(np.random.random(1) * 2 - 1) * size, 2
        )
        composition[element] = max(composition[element], 0)

    elements = list(composition.keys())
    if len(composition) > 1:
        for element in elements:
            if composition[element] < 0.0001:
                if (
                    constraints is not None
                    and element in constraints["percentages"]
                    and constraints["percentages"][element]["precedence"] > 0
                ):
                    continue
                del composition[element]

    if np.random.random(1) > 0.1:
        allowed_elements = list(mg.periodic_table.elements.keys())
        if constraints is not None and "allowed_elements" in constraints:
            allowed_elements = constraints["allowed_elements"][:]
        for element in composition:
            if element in allowed_elements:
                allowed_elements.remove(element)
        if len(allowed_elements) > 0:
            element = np.random.choice(allowed_elements)
            existing_element = np.random.choice(list(composition.keys()))
            composition[element] = composition[existing_element]
            del composition[existing_element]

    if np.random.random(1) > 0.1:
        allowed_elements = list(mg.periodic_table.elements.keys())
        if constraints is not None and "allowed_elements" in constraints:
            allowed_elements = constraints["allowed_elements"][:]
        for element in composition:
            if element in allowed_elements:
                allowed_elements.remove(element)
        if len(allowed_elements) > 0:
            element = np.random.choice(allowed_elements)
            composition[element] = round(float(np.random.random(1)) * size, 2)

    if len(composition) > 1 and np.random.random(1) > 0.1:
        not_deleted = True
        deletable = list(composition.keys())
        while not_deleted or len(deletable) > 1:
            to_delete = np.random.choice(deletable)
            deletable.remove(to_delete)

            if not (
                constraints is not None
                and to_delete in constraints["percentages"]
                and constraints["percentages"][to_delete]["precedence"] > 0
            ):
                del composition[to_delete]
                not_deleted = False
                break

    if structure is not None and np.random.random(1) > 0.1:
        structure = get_random_prototype()

    new_alloy = mg.Alloy(
        composition, constraints=constraints, structure=structure
    )
    return new_alloy
