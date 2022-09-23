from __future__ import annotations
import copy
import re
from typing import Union, Callable, Optional
from collections import OrderedDict

import numpy as np
import elementy


class Alloy:
    """An alloy, a mixture of chemical elements with specific percentages.

    Attributes:
        composition: Dictionary matching element symbols to atomic
                            percentages.
        constraints: Dictionary of constraints to follow when adjusting
                            atomic percentages.

    """

    class Composition(dict):
        """Atomic percentages of elements in an alloy.

        Attributes:
            on_change (Callable): Callback function enabling parent
                                  to act on composition changes

        """

        def __init__(self, value: dict, on_change: Callable, *args, **kwargs):
            super().__init__(value, *args, **kwargs)
            self.on_change = on_change

        def __setitem__(self, element: str, percentage: float):
            """
            Set the percentage value of an element in the composition.
            Remove elements from the composition if below minimum threshold.
            """
            if percentage >= 0.01:
                super().__setitem__(element, percentage)
            else:
                if element in self.keys():
                    super().__delitem__(element)
            self.on_change(change_type="set")

        def __delitem__(self, element):
            super().__delitem__(element)
            self.on_change(change_type="del")

    def __init__(
        self,
        composition: Union[str, dict, Alloy],
        constraints: Union[dict, None] = None,
        rescale: bool = True,
    ):

        self.composition = parse_composition(composition)
        self.constraints = None

        if rescale:
            self.clamp_composition()
            self.round_composition()

        if constraints is not None:
            self.constraints = parse_constraints(**constraints)
            if rescale:
                self.rescale()

    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        return self.to_string() == other.to_string()

    def __hash__(self):
        return hash(self.to_string())

    @property
    def composition(self) -> Composition:
        """Dictionary of elements and percentages in the alloy."""
        return self._composition

    @composition.setter
    def composition(self, value):
        if isinstance(value, (dict, OrderedDict)):
            value = self.Composition(value, self.on_composition_change)
        self._composition = value

    def on_composition_change(self, change_type=None):
        """Called when composition property changes."""
        self.determine_percentage_constraints()

        if change_type == "del":
            self.clamp_composition()
            self.round_composition()

    @property
    def elements(self) -> list:
        """List of elements in the alloy."""
        return list(self.composition.keys())

    def rescale(self):
        """Adjust elemental percentages to match constraints

        All alloys are constrained such that element percentages sum
        to 1.0. Additional constraints include:

        - Minimum number of unique elements in an alloy.
        - Maximum number of unique elements in an alloy.
        - Maximum and minimum percentage values per element.
        - Precedence order of elements.
        """

        constraints_applied = False
        while not self.constraints_satisfied():

            constraints_applied = True

            precedence = {}
            for element in self.constraints["local_percentages"]:
                if self.constraints["local_percentages"][element]["min"] > 0:
                    if element not in self.composition:
                        self.composition[element] = 0.01

                precedence[element] = self.constraints["local_percentages"][
                    element
                ]["precedence"]

            precedence_order = sorted(
                precedence, key=precedence.get, reverse=True
            )
            reverse_precedence_order = sorted(precedence, key=precedence.get)

            for element in precedence_order:
                if element not in self.composition:
                    if (
                        self.constraints["local_percentages"][element]["min"]
                        > 0
                    ):
                        self.composition[element] = self.constraints[
                            "local_percentages"
                        ][element]["min"]
                    else:
                        continue

                if (
                    self.composition[element]
                    < self.constraints["local_percentages"][element]["min"]
                ):
                    for other_element in reverse_precedence_order:
                        if (
                            element != other_element
                            and other_element in self.composition
                        ):

                            if (
                                self.composition[other_element]
                                > self.constraints["local_percentages"][
                                    other_element
                                ]["max"]
                            ):

                                element_deficit = (
                                    self.constraints["local_percentages"][
                                        element
                                    ]["min"]
                                    - self.composition[element]
                                )

                                other_element_surplus = (
                                    self.composition[other_element]
                                    - self.constraints["local_percentages"][
                                        other_element
                                    ]["max"]
                                )

                                # print("A")
                                # print(self.composition)
                                # print(element, element_deficit)
                                # print(other_element, other_element_surplus)
                                # print()

                                if (
                                    element_deficit >= other_element_surplus
                                    and other_element_surplus > 0
                                ):
                                    self.composition[
                                        element
                                    ] += other_element_surplus
                                    self.composition[
                                        other_element
                                    ] -= other_element_surplus
                                else:
                                    self.composition[
                                        element
                                    ] += element_deficit
                                    self.composition[
                                        other_element
                                    ] -= element_deficit

                                if element not in self.composition:
                                    self.composition[
                                        element
                                    ] = self.constraints["local_percentages"][
                                        element
                                    ][
                                        "min"
                                    ]
                                if (
                                    self.composition[element]
                                    >= self.constraints["local_percentages"][
                                        element
                                    ]["min"]
                                ):
                                    break

                if element not in self.composition:
                    if (
                        self.constraints["local_percentages"][element]["min"]
                        > 0
                    ):
                        self.composition[element] = self.constraints[
                            "local_percentages"
                        ][element]["min"]
                    else:
                        continue

                if (
                    self.composition[element]
                    < self.constraints["local_percentages"][element]["min"]
                ):

                    for other_element in sorted(
                        self.composition.keys(),
                        key=lambda k: np.random.random(),
                    ):

                        if other_element != element:

                            other_element_surplus = self.composition[
                                other_element
                            ]
                            if (
                                other_element
                                in self.constraints["local_percentages"]
                            ):
                                if (
                                    self.constraints["local_percentages"][
                                        element
                                    ]["precedence"]
                                    < self.constraints["local_percentages"][
                                        other_element
                                    ]["precedence"]
                                ):
                                    continue

                                other_element_surplus -= self.constraints[
                                    "local_percentages"
                                ][other_element]["min"]

                            if (
                                normal_round(
                                    other_element_surplus,
                                    self.constraints["sigfigs"] + 1,
                                )
                                > 0
                            ):

                                element_deficit = (
                                    self.constraints["local_percentages"][
                                        element
                                    ]["min"]
                                    - self.composition[element]
                                )

                                # print("B")
                                # print(self.composition)
                                # print(element, element_deficit)
                                # print(other_element, other_element_surplus)
                                # print()

                                if (
                                    element_deficit
                                    >= self.composition[other_element]
                                ):
                                    self.composition[
                                        element
                                    ] += other_element_surplus
                                    self.composition[
                                        other_element
                                    ] -= other_element_surplus
                                else:
                                    self.composition[
                                        element
                                    ] += element_deficit
                                    self.composition[
                                        other_element
                                    ] -= element_deficit

                                if element not in self.composition:
                                    self.composition[
                                        element
                                    ] = self.constraints["local_percentages"][
                                        element
                                    ][
                                        "min"
                                    ]
                                if (
                                    self.composition[element]
                                    >= self.constraints["local_percentages"][
                                        element
                                    ]["min"]
                                ):
                                    break

                if element not in self.composition:
                    if (
                        self.constraints["local_percentages"][element]["min"]
                        > 0
                    ):
                        self.composition[element] = self.constraints[
                            "local_percentages"
                        ][element]["min"]
                    else:
                        continue

                if (
                    self.composition[element]
                    > self.constraints["local_percentages"][element]["max"]
                ):
                    for other_element in reverse_precedence_order:
                        if (
                            element != other_element
                            and other_element in self.composition
                        ):

                            if (
                                self.composition[other_element]
                                < self.constraints["local_percentages"][
                                    other_element
                                ]["min"]
                            ):
                                element_surplus = (
                                    self.composition[element]
                                    - self.constraints["local_percentages"][
                                        element
                                    ]["max"]
                                )

                                other_element_deficit = (
                                    self.constraints["local_percentages"][
                                        other_element
                                    ]["min"]
                                    - self.composition[other_element]
                                )

                                # print("C")
                                # print(self.composition)
                                # print(element, element_surplus)
                                # print(other_element, other_element_deficit)
                                # print()

                                if element_surplus >= other_element_deficit:
                                    self.composition[
                                        element
                                    ] -= other_element_deficit
                                    self.composition[
                                        other_element
                                    ] += element_surplus
                                else:
                                    self.composition[
                                        element
                                    ] -= element_surplus
                                    self.composition[
                                        other_element
                                    ] += element_surplus

                                if element not in self.composition:
                                    self.composition[
                                        element
                                    ] = self.constraints["local_percentages"][
                                        element
                                    ][
                                        "max"
                                    ]
                                if (
                                    self.composition[element]
                                    <= self.constraints["local_percentages"][
                                        element
                                    ]["max"]
                                ):
                                    break

                if element not in self.composition:
                    if (
                        self.constraints["local_percentages"][element]["min"]
                        > 0
                    ):
                        self.composition[element] = self.constraints[
                            "local_percentages"
                        ][element]["min"]
                    else:
                        continue

                if (
                    self.composition[element]
                    > self.constraints["local_percentages"][element]["max"]
                ):
                    for other_element in sorted(
                        self.composition.keys(),
                        key=lambda k: np.random.random(),
                    ):
                        if other_element != element:

                            if (
                                other_element
                                in self.constraints["local_percentages"]
                            ):
                                other_element_deficit = (
                                    self.constraints["local_percentages"][
                                        other_element
                                    ]["max"]
                                    - self.composition[other_element]
                                )
                            else:
                                other_element_deficit = (
                                    1.0 - self.composition[other_element]
                                )

                            element_surplus = (
                                self.composition[element]
                                - self.constraints["local_percentages"][
                                    element
                                ]["max"]
                            )

                            element_surplus = np.max(
                                [
                                    element_surplus,
                                    self.constraints["percentage_step"],
                                ]
                            )
                            other_element_deficit = np.max(
                                [
                                    other_element_deficit,
                                    self.constraints["percentage_step"],
                                ]
                            )

                            # print("D")
                            # print(self.composition)
                            # print(element, element_surplus)
                            # print(other_element, other_element_deficit)
                            # print()

                            if (
                                element_surplus >= other_element_deficit
                                and other_element_deficit > 0
                            ):
                                self.composition[
                                    element
                                ] -= other_element_deficit
                                self.composition[
                                    other_element
                                ] += other_element_deficit
                            else:
                                self.composition[element] -= element_surplus
                                self.composition[
                                    other_element
                                ] += element_surplus

                            if element not in self.composition:
                                self.composition[element] = self.constraints[
                                    "local_percentages"
                                ][element]["max"]
                            if (
                                self.composition[element]
                                <= self.constraints["local_percentages"][
                                    element
                                ]["max"]
                            ):
                                break

            if len(self.composition) > self.constraints["max_elements"]:

                excess = (
                    len(self.composition) - self.constraints["max_elements"]
                )

                toDelete = []
                ordered_elements = sorted(
                    self.composition, key=self.composition.get
                )
                for element in ordered_elements:
                    if element in self.constraints["local_percentages"]:
                        if (
                            self.constraints["local_percentages"][element][
                                "min"
                            ]
                            == 0
                        ):
                            toDelete.append(element)
                    else:
                        toDelete.append(element)

                    if len(toDelete) == excess:
                        break

                for element in toDelete:
                    del self.composition[element]

            elif len(self.composition) < self.constraints["min_elements"]:

                while len(self.composition) < self.constraints["min_elements"]:

                    element_to_add = np.random.choice(
                        self.constraints["allowed_elements"], 1
                    )[0]
                    if element_to_add not in self.composition:
                        self.composition[element_to_add] = np.random.uniform()

            self.clamp_composition()

        if not constraints_applied:
            self.clamp_composition()
        self.round_composition()

    def constraints_satisfied(self) -> bool:
        """Check for satisfaction of the constraints acting on an alloy"""

        satisfied = True
        if self.constraints is not None:

            discrepancy = np.abs(
                1
                - multiple_round(
                    sum(self.composition.values()),
                    self.constraints["percentage_step"],
                )
            )
            if discrepancy > self.constraints["percentage_step"]:
                # print("Sum != 1", sum(self.composition.values()), discrepancy)
                # print(self.composition)
                # print()
                satisfied = False

            if satisfied:
                for element in self.constraints["local_percentages"]:
                    if element in self.composition:
                        if (
                            self.composition[element]
                            < self.constraints["local_percentages"][element][
                                "min"
                            ]
                        ):
                            # print("element below min", element,
                            #       self.composition[element], self.constraints['local_percentages'][element]['min'])
                            # print(self.composition)
                            # print()
                            satisfied = False
                            break
                        elif (
                            self.composition[element]
                            > self.constraints["local_percentages"][element][
                                "max"
                            ]
                        ):
                            # print("element above max", element,
                            #       self.composition[element], self.constraints['local_percentages'][element]['max'])
                            # print(self.composition)
                            # print()
                            satisfied = False
                            break
                    elif (
                        self.constraints["local_percentages"][element]["min"]
                        > 0.0
                    ):
                        # print("element missing", element,
                        #       self.constraints['local_percentages'][element]['min'])
                        # print(self.composition)
                        # print()
                        satisfied = False
                        break

            if satisfied:
                if len(self.composition) > self.constraints["max_elements"]:
                    satisfied = False
                    # print("too many elements")
                    # print(self.composition)
                    # print()
                elif len(self.composition) < self.constraints["min_elements"]:
                    satisfied = False
                    # print("too few elements")
                    # print(self.composition)
                    # print()

        return satisfied

    def clamp_composition(self):
        """Adjust elemental percentages such that they sum to 1.0"""

        total_percentage = sum(self.composition.values())

        for element in self.elements:
            clamped_value = self.composition[element] / total_percentage
            if self.constraints is not None:
                if element in self.constraints["percentages"]:
                    self.composition[element] = max(
                        clamped_value,
                        self.constraints["percentages"][element]["min"],
                    )
                else:
                    self.composition[element] = clamped_value
            else:
                self.composition[element] = clamped_value

    def determine_percentage_constraints(self):
        """Determine the current constraints on an alloy composition.

        When precedence constraints are acting, the maximum and
        minimum percentage values for each element depend on the
        others.
        """

        if self.constraints is None:
            return

        tmp_percentages = copy.deepcopy(self.constraints["percentages"])

        lowest_precedence = {
            "element": None,
            "precedence": np.Inf,
            "percentage": np.Inf,
        }
        for element in self.constraints["percentages"]:
            if element in self.composition:
                if (
                    self.constraints["percentages"][element]["precedence"]
                    <= lowest_precedence["precedence"]
                    and self.constraints["percentages"][element]["precedence"]
                    > 0
                    and self.composition[element]
                    < lowest_precedence["percentage"]
                ):

                    lowest_precedence["precedence"] = self.constraints[
                        "percentages"
                    ][element]["precedence"]
                    lowest_precedence["element"] = element
                    lowest_precedence["percentage"] = self.composition[element]

            if (
                len(
                    self.constraints["percentages"][element][
                        "superior_elements"
                    ]
                )
                > 0
            ):
                superior_elements = []
                for e in self.constraints["percentages"][element][
                    "superior_elements"
                ]:
                    if e in self.composition:
                        superior_elements.append(self.composition[e])
                if len(superior_elements) > 0:
                    tmp_percentages[element]["max"] = min(superior_elements)
                else:
                    tmp_percentages[element]["max"] = 0

        if lowest_precedence["element"] is not None:
            for element in self.composition:
                if element not in tmp_percentages:
                    maxPercent = lowest_precedence["percentage"]

                    tmp_percentages[element] = {
                        "max": maxPercent,
                        "min": 0,
                        "precedence": 0,
                        "superior_elements": [],
                    }

                    for other_element in tmp_percentages:
                        if element != other_element:
                            if (
                                tmp_percentages[element]["precedence"]
                                < tmp_percentages[other_element]["precedence"]
                            ):
                                tmp_percentages[element][
                                    "superior_elements"
                                ].append(other_element)

        self.constraints["local_percentages"] = tmp_percentages

    def to_string(self) -> str:
        """Convert the alloy composition dict to a string"""

        composition_str = ""
        for element in self.elements:
            percentage_str = str(self.composition[element] * 100.0)

            split_str = percentage_str.split(".")
            decimal = split_str[1]
            if decimal == "0":
                percentage_str = split_str[0]
            else:
                decimal_places = len(
                    str(self.composition[element]).split(".")[1]
                )
                percentage_str = str(
                    round(float(percentage_str), decimal_places)
                )

                split_str = percentage_str.split(".")
                decimal = split_str[1]
                if decimal == "0":
                    percentage_str = split_str[0]

            composition_str += element + percentage_str

        return composition_str

    def to_pretty_string(self) -> str:
        """Convert alloy composition to string with LaTeX formatting of subscripts"""
        numbers = re.compile(r"(\d+)")
        return numbers.sub(r"$_{\1}$", self.to_string())

    def round_composition(self):
        """Round elemental percentages in composition while maintaining sum"""

        if len(self.composition) == 0:
            return
        elif len(self.composition) == 1:
            self.composition[self.elements[0]] = 1.0

        if self.constraints is not None:
            sigfigs = self.constraints["sigfigs"]
        else:
            sigfigs = 3

        integer_parts = []
        decimal_parts = []

        elements = list(self.composition.keys())
        for element in elements:

            rounded_percentage = normal_round(
                self.composition[element], sigfigs
            )

            if rounded_percentage > 0:

                percentage = str(self.composition[element] * (10**sigfigs))
                split_percentage = percentage.split(".")

                integer_parts.append(int(split_percentage[0]))

                if len(split_percentage) > 1:
                    decimal_parts.append(
                        float(percentage) - float(split_percentage[0])
                    )
                else:
                    decimal_parts.append(0.0)

        undershoot = (10**sigfigs) - sum(integer_parts)

        if undershoot > 0:
            if self.constraints is not None:

                precedence = {}
                for element in elements:
                    if element in self.constraints["local_percentages"]:
                        precedence[element] = self.constraints[
                            "local_percentages"
                        ][element]["precedence"]
                    else:
                        precedence[element] = 0
                precedence_order = sorted(
                    precedence, key=precedence.get, reverse=True
                )

                filtered_precedence_order = []
                for element in precedence_order:
                    if element in self.composition:
                        filtered_precedence_order.append(element)
            else:
                filtered_precedence_order = list(self.composition.keys())

            i = 0
            while undershoot > 0:
                decimal_part_index = list(self.composition.keys()).index(
                    filtered_precedence_order[i]
                )

                constraints_violated = False
                if self.constraints is not None:
                    if (
                        filtered_precedence_order[i]
                        in self.constraints["local_percentages"]
                    ):
                        if (integer_parts[decimal_part_index] + 1) / (
                            10**sigfigs
                        ) > self.constraints["local_percentages"][
                            filtered_precedence_order[i]
                        ][
                            "max"
                        ]:
                            constraints_violated = True

                if not constraints_violated:
                    integer_parts[decimal_part_index] += 1
                    undershoot -= 1
                i += 1

                if i >= len(filtered_precedence_order):
                    i = 0

            elements = list(self.composition.keys())

            i = 0
            for element in elements:
                self.composition[element] = normal_round(
                    integer_parts[i] / (10**sigfigs), sigfigs
                )
                i += 1

        else:

            elements = list(self.composition.keys())
            i = 0
            for element in elements:

                rounded_value = integer_parts[i] / (10**sigfigs)

                if self.constraints is not None:
                    if element in self.constraints["local_percentages"]:
                        self.composition[element] = max(
                            self.constraints["local_percentages"][element][
                                "min"
                            ],
                            rounded_value,
                        )
                    else:
                        self.composition[element] = rounded_value
                else:
                    self.composition[element] = rounded_value

                i += 1


def parse_composition(composition: Union[str, dict, Alloy]) -> dict:
    """Parse elemental percentages of an alloy from input"""
    if isinstance(composition, str):
        return parse_composition_string(composition)
    elif isinstance(composition, dict):
        return parse_composition_dict(composition)
    elif isinstance(composition, Alloy):
        return composition.composition


def parse_composition_string(composition_string: str) -> dict:
    """Parse elemental percentages of an alloy from a string"""

    composition = {}
    if "(" in composition_string:
        major_composition = composition_string.split(")")[0].split("(")[1]

        major_composition_percentage = (
            float(
                re.split(r"(\d+(?:\.\d+)?)", composition_string.split(")")[1])[
                    1
                ]
            )
            / 100.0
        )

        split_major_composition = re.findall(
            r"[A-Z][^A-Z]*", major_composition
        )

        for element_percentage in split_major_composition:
            split_element_percentage = re.split(
                r"(\d+(?:\.\d+)?)", element_percentage
            )
            composition[split_element_percentage[0]] = (
                float(split_element_percentage[1]) / 100.0
            ) * major_composition_percentage

        minor_composition = composition_string.split(")")[1][
            len(str(int(major_composition_percentage * 100))) :
        ]
        split_minor_composition = re.findall(
            r"[A-Z][^A-Z]*", minor_composition
        )
        for element_percentage in split_minor_composition:
            split_element_percentage = re.split(
                r"(\d+(?:\.\d+)?)", element_percentage
            )

            decimal_places = 2
            if "." in str(split_element_percentage[1]):
                decimal_places += len(
                    str(split_element_percentage[1]).split(".")[1]
                )

            composition[split_element_percentage[0]] = round(
                float(split_element_percentage[1]) / 100.0, decimal_places
            )

    else:

        split_composition = re.findall(r"[A-Z][^A-Z]*", composition_string)

        for element_percentage in split_composition:
            split_element_percentage = re.split(
                r"(\d+(?:\.\d+)?)", element_percentage
            )

            if len(split_element_percentage) > 1:
                decimal_places = 2
                if "." in str(split_element_percentage[1]):
                    decimal_places += len(
                        str(split_element_percentage[1]).split(".")[1]
                    )

                composition[split_element_percentage[0]] = round(
                    float(split_element_percentage[1]) / 100.0, decimal_places
                )
            else:
                composition[split_element_percentage[0]] = 1.0 / len(
                    split_composition
                )

    return filter_order_composition(composition)


def parse_composition_dict(composition: dict) -> dict:
    """Parse elemental percentages of an alloy from a dict"""

    tmp_composition = copy.deepcopy(composition)

    needRescale = False
    for element in tmp_composition:
        if tmp_composition[element] > 1:
            needRescale = True
            break

    if needRescale:
        for element in tmp_composition:
            tmp_composition[element] /= 100.0

    return filter_order_composition(tmp_composition)


def filter_order_composition(composition: dict) -> OrderedDict:
    """Filter & order elements in an alloy composition

    Elements with percentage less than zero are filtered out.
    An OrderedDict is used to sort the composition in descending
    order of elemental percentage.
    """

    filtered_composition = {}
    for element in composition:
        if composition[element] > 0:
            filtered_composition[element] = composition[element]

    ordered_composition = OrderedDict()
    for element in sorted(
        filtered_composition, key=filtered_composition.get, reverse=True
    ):
        ordered_composition[element] = filtered_composition[element]

    return ordered_composition


def parse_constraints(
    min_elements: int = 1,
    max_elements: int = 10,
    percentages: dict = {},
    allowed_elements: list = [e for e in elementy.PeriodicTable().elements],
    disallowed_elements: list = [],
    sigfigs: int = 3,
    percentage_step: float = 0.01,
) -> dict:
    """Parse constraint rules from input

    Args:
        min_elements: Minimum number of elements in an alloy
        max_elements: Maximum number of elements in an alloy
        percentages: Dict of maximum and minimum percentages
                            per element
        allowed_elements: List of elements allowed in an alloy
        disallowed_elements: List of elements not allowed in an
                             alloy
        sigfigs: Number of significant figures to consider for
                       percentages
        percentage_step: Increment between percentages
    """

    if not isinstance(percentages, dict):
        if isinstance(percentages, list):
            tmp_percentages = {}
            for element in percentages:
                tmp_percentages[element] = {}
            percentages = tmp_percentages

    for element in percentages:
        if "min" not in percentages[element]:
            percentages[element]["min"] = 0.0
        else:
            percentages[element]["min"] = max(percentages[element]["min"], 0.0)

        if "max" not in percentages[element]:
            percentages[element]["max"] = 1.0
        else:
            percentages[element]["max"] = min(percentages[element]["max"], 1.0)

        if "precedence" not in percentages[element]:
            percentages[element]["precedence"] = 0

    for element in percentages:
        percentages[element]["superior_elements"] = []
        for other_element in percentages:
            if element != other_element:
                if (
                    percentages[element]["precedence"]
                    < percentages[other_element]["precedence"]
                ):
                    percentages[element]["superior_elements"].append(
                        other_element
                    )

    min_sum = sum([percentages[e]["min"] for e in percentages])
    if min_sum > 1:
        print(
            "Impossible constraints, mins for each element sum greater than 1"
        )

    for element in disallowed_elements:
        if element in allowed_elements:
            allowed_elements.remove(element)

    return {
        "percentages": percentages,
        "local_percentages": percentages,
        "allowed_elements": allowed_elements,
        "min_elements": min_elements,
        "max_elements": max_elements,
        "sigfigs": sigfigs,
        "percentage_step": percentage_step,
    }


def normal_round(num: float, ndigits: int = 0) -> float:
    """Rounds a float to the specified number of decimal places.

    Args:
        num: the value to round
        ndigits: the number of digits to round to
    """
    if ndigits == 0:
        return int(num + 0.5)
    else:
        digit_value = 10**ndigits
        return int(num * digit_value + 0.5) / digit_value


def multiple_round(
    num: float, multiple: Union[float, int]
) -> Union[float, int]:
    """Round a number to the nearest multiple of another number.

    Args:
        num: Value to round
        multiple: Multiple-of to round towards
    """
    return multiple * round(num / multiple)
