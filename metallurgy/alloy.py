from __future__ import annotations
import copy
import re
from typing import Union, Callable, Optional
from collections import OrderedDict, Counter

import numpy as np
import elementy


class Alloy:
    """An alloy, a mixture of chemical elements with specific percentages.

    :group: alloy

    Attributes
    ----------

    composition : dict
        Dictionary matching element symbols to atomic percentages.
    constraints : dict
        Dictionary of constraints to follow when adjusting atomic  percentages.

    """

    class Composition(OrderedDict):
        """Atomic percentages of elements in an alloy.

        :group: alloy

        Attributes
        ----------

        on_change : Callable
            Callback function enabling parent to act on composition changes

        """

        def __init__(self, value: dict, on_change: Callable, *args, **kwargs):
            super().__init__(value, *args, **kwargs)
            self.on_change = on_change

        def __setitem__(
            self, element: str, percentage: float, respond_to_change=True
        ):
            """
            Set the percentage value of an element in the composition.
            Remove elements from the composition if below minimum threshold.
            """
            if percentage >= 0.0001:
                super().__setitem__(element, percentage)
            else:
                if element in self.keys():
                    super().__delitem__(element)
            if hasattr(self, "on_change") and respond_to_change:
                self.on_change()

        def __delitem__(self, element, respond_to_change=True):
            super().__delitem__(element)
            if hasattr(self, "on_change") and respond_to_change:
                self.on_change()

    def __init__(
        self,
        composition: Union[str, dict, Alloy],
        constraints: Union[dict, None] = None,
        rescale: bool = True,
    ):

        self.composition = parse_composition(composition)
        if self.composition is None:
            raise Exception("Invalid composition:", composition)

        self.constraints = None

        if rescale:
            self.rescale()

        if constraints is not None:
            self.constraints = parse_constraints(**constraints)
            if self.num_elements == 1:
                if self.elements[0] in self.constraints["percentages"]:
                    self.constraints["percentages"][self.elements[0]][
                        "max"
                    ] = 1
            if rescale:
                self.rescale()

    def __repr__(self):
        return self.to_string()

    def __eq__(self, other):
        if isinstance(other, Alloy):
            return self.to_string() == other.to_string()
        elif isinstance(other, (str, dict)):
            return self.to_string() == Alloy(other).to_string()
        else:
            return False

    def __add__(self, other):
        from . import generate

        return generate.mixture([self, other])

    def __hash__(self):
        return hash(self.to_string())

    @property
    def composition(self) -> Composition:
        """Dictionary of elements and percentages in the alloy.

        :group: alloy
        """
        return self._composition

    @composition.setter
    def composition(self, value):
        if isinstance(value, (dict, OrderedDict)):
            value = self.Composition(value, self.on_composition_change)
        self._composition = value

    def on_composition_change(self):
        """Called when composition property changes.

        :group: alloy.utils
        """
        self.determine_percentage_constraints()

        if not hasattr(self, "rescaling"):
            self.rescale()

    @property
    def elements(self) -> list:
        """List of elements in the alloy.

        :group: alloy
        """
        return list(self.composition.keys())

    @property
    def num_elements(self) -> int:
        """Number of elements in the alloy.

        :group: alloy
        """
        return len(self.elements)

    @property
    def total_percentage(self) -> float:
        """Sum of percentages in the alloy composition.

        :group: alloy
        """
        return sum(self.composition.values())

    def add_element(self, element: str, percentage: Optional[float] = 0.0):
        """Adds an element to the alloy composition.

        :group: alloy

        Parameters
        ----------

        element
            Element to be added.
        percentage
            Percentage of the new element. If zero or not set, is given the
            value of 1.0/(number of elements +1).

        """
        if element not in self.elements:
            if percentage == 0.0:
                percentage = 1.0 / (self.num_elements + 1)

            self.composition[element] = percentage

    def remove_element(self, element: str):
        """Removes an element from the alloy composition.

        :group: alloy

        Parameters
        ----------

        element
            Element to be removed.

        """
        if element in self.elements:
            del self.composition[element]

    def ensure_constrained_elements_present(self):
        """Adds to the composition any elements with minimum percentage
        constraints that are missing

        :group: alloy.utils
        """
        for element in self.constraints["local_percentages"]:
            if element not in self.composition:
                if self.constraints["local_percentages"][element]["min"] > 0:
                    self.composition[element] = self.constraints[
                        "local_percentages"
                    ][element]["min"]

    def rescale(self):
        """Adjust elemental percentages to match constraints

        All alloys are constrained such that element percentages sum
        to 1.0. Additional constraints include:

        - Minimum number of unique elements in an alloy.
        - Maximum number of unique elements in an alloy.
        - Maximum and minimum percentage values per element.
        - Precedence order of elements.

        :group: alloy.utils
        """

        if len(self.composition) < 1:
            return

        self.rescaling = True

        constraints_applied = False
        while not self.constraints_satisfied():

            self.determine_percentage_constraints()

            constraints_applied = True

            precedence = {}
            no_precedence = []

            self.ensure_constrained_elements_present()
            for element in self.composition:
                if element in self.constraints["local_percentages"]:
                    if (
                        self.constraints["local_percentages"][element]["min"]
                        > 0
                    ):
                        precedence[element] = self.constraints[
                            "local_percentages"
                        ][element]["precedence"]

                if element not in precedence:
                    no_precedence.append(element)

            precedence_order = (
                sorted(precedence, key=precedence.get, reverse=True)
                + no_precedence
            )
            reverse_precedence_order = precedence_order[::-1]

            for element in precedence_order:
                if element not in self.constraints["local_percentages"]:
                    continue

                for direction in ["min", "max"]:
                    if element_is_in_range(
                        element,
                        self.composition,
                        self.constraints,
                        direction,
                        inclusive=True,
                    ):
                        continue

                    for other_element in reverse_precedence_order:
                        if (
                            element != other_element
                            and other_element in self.composition
                        ):
                            if not element_is_in_range(
                                other_element,
                                self.composition,
                                self.constraints,
                                direction,
                                inclusive=False,
                            ):
                                continue

                            if direction == "min":
                                donate_percentage(
                                    self.composition,
                                    self.constraints,
                                    other_element,
                                    element,
                                )
                            else:
                                donate_percentage(
                                    self.composition,
                                    self.constraints,
                                    element,
                                    other_element,
                                )

                            self.ensure_constrained_elements_present()

                            if element_is_in_range(
                                element,
                                self.composition,
                                self.constraints,
                                direction,
                            ):
                                break

            self.constrain_num_elements()
            self.clamp_composition()
            self.round_composition()

        if not constraints_applied:
            self.clamp_composition()
        self.round_composition()

        self.reorder_composition()

        delattr(self, "rescaling")

    def reorder_composition(self):
        ordered_elements = sorted(
            self.composition, key=self.composition.get, reverse=True
        )
        for element in ordered_elements:
            self.composition.move_to_end(element)

    def constrain_max_elements(self):
        """Removes elements from an alloy if there are more elements than
        allowed by the max_elements constraint."""
        if len(self.composition) > self.constraints["max_elements"]:

            excess = len(self.composition) - self.constraints["max_elements"]

            toDelete = []
            ordered_elements = sorted(
                self.composition, key=self.composition.get
            )
            for element in ordered_elements:
                if element in self.constraints["local_percentages"]:
                    if (
                        self.constraints["local_percentages"][element]["min"]
                        == 0
                    ):
                        toDelete.append(element)
                else:
                    toDelete.append(element)

                if len(toDelete) == excess:
                    break

            for element in toDelete:
                del self.composition[element]

    def constrain_min_elements(self):
        """Adds elements to an alloy if there are fewer elements than
        allowed by the min_elements constraint."""
        if len(self.composition) < self.constraints["min_elements"]:

            while len(self.composition) < self.constraints["min_elements"]:

                element_to_add = np.random.choice(
                    self.constraints["allowed_elements"], 1
                )[0]
                if element_to_add not in self.composition:
                    self.composition[element_to_add] = np.random.uniform()

    def constrain_num_elements(self):
        """Applies max and min element count constraints.
        :group: alloy.utils
        """
        self.constrain_max_elements()
        self.constrain_min_elements()

    def constraints_satisfied(self) -> bool:
        """Check for satisfaction of the constraints acting on an alloy.

        :group: alloy.utils
        """

        satisfied = True
        if self.constraints is not None:

            discrepancy = np.abs(
                1
                - multiple_round(
                    self.total_percentage,
                    self.constraints["percentage_step"],
                    self.constraints["digits"],
                )
            )

            if discrepancy > self.constraints["percentage_step"]:
                # print("Sum != 1", self.total_percentage, discrepancy)
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
                            # print(
                            #     "element below min",
                            #     element,
                            #     self.composition[element],
                            #     self.constraints["local_percentages"][element][
                            #         "min"
                            #     ],
                            # )
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
                            # print(
                            #     "element above max",
                            #     element,
                            #     self.composition[element],
                            #     self.constraints["local_percentages"][element][
                            #         "max"
                            #     ],
                            # )
                            # print(self.composition)
                            # print()
                            satisfied = False
                            break
                        elif (
                            "superior_elements"
                            in self.constraints["local_percentages"][element]
                        ):
                            for superior_element in self.constraints[
                                "local_percentages"
                            ][element]["superior_elements"]:
                                if superior_element in self.composition:
                                    if (
                                        self.composition[element]
                                        > self.composition[superior_element]
                                    ):
                                        # print(
                                        #     "element above superior",
                                        #     element,
                                        #     superior_element,
                                        #     self.composition[element],
                                        #     self.constraints[
                                        #         "local_percentages"
                                        #     ][element]["max"],
                                        #     self.composition[superior_element],
                                        # )
                                        # print(self.composition)
                                        # print(self.constraints)
                                        # print()
                                        satisfied = False
                                        break
                                if not satisfied:
                                    break

                    elif (
                        self.constraints["local_percentages"][element]["min"]
                        > 0.0
                    ):
                        # print(
                        #     "element missing",
                        #     element,
                        #     self.constraints["local_percentages"][element][
                        #         "min"
                        #     ],
                        # )
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
        """Adjust elemental percentages such that they sum to 1

        :group: alloy.utils
        """

        digits = 4
        percentage_step = 0.01
        if self.constraints is not None:
            if "digits" in self.constraints:
                digits = self.constraints["digits"]
            if "percentage_step" in self.constraints:
                percentage_step = self.constraints["percentage_step"]

        while (
            np.abs(
                1
                - multiple_round(
                    self.total_percentage, percentage_step, digits
                )
            )
            >= percentage_step
        ):

            current_total = self.total_percentage
            elements = self.elements

            clamped_rounded_total = 0
            for element in elements:
                clamped_value = self.composition[element] / current_total

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

                if element in self.composition:
                    clamped_rounded_total += multiple_round(
                        self.composition[element], percentage_step, digits
                    )

            while (
                round(np.abs(1 - clamped_rounded_total), digits)
                >= percentage_step
            ):
                elements = self.elements
                for element in elements:
                    if element not in self.composition:
                        continue

                    if self.constraints is not None:
                        if element in self.constraints["percentages"]:
                            change = max(
                                [
                                    percentage_step,
                                    max(
                                        [
                                            0,
                                            self.constraints["percentages"][
                                                element
                                            ]["max"]
                                            - self.composition[element],
                                        ]
                                    ),
                                ]
                            )
                        else:
                            change = percentage_step
                    else:
                        change = percentage_step

                    change = min([change, np.abs(1 - clamped_rounded_total)])
                    if clamped_rounded_total > 1:
                        change *= -1

                    change = multiple_round(change, percentage_step, digits)

                    self.composition.__setitem__(
                        element,
                        self.composition[element] + change,
                        respond_to_change=False,
                    )
                    clamped_rounded_total += change
                    if np.abs(1 - clamped_rounded_total) > percentage_step / 2:
                        break

    def determine_percentage_constraints(self):
        """Determine the current constraints on an alloy composition.

        When precedence constraints are acting, the maximum and
        minimum percentage values for each element depend on the
        others.

        :group: alloy.utils
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
                element_constraint = self.constraints["percentages"][element]
                if (
                    element_constraint["precedence"]
                    <= lowest_precedence["precedence"]
                    and element_constraint["precedence"] > 0
                    and self.composition[element]
                    < lowest_precedence["percentage"]
                ):

                    lowest_precedence["precedence"] = element_constraint[
                        "precedence"
                    ]
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
                    tmp_percentages[element]["max"] = min(
                        [
                            self.constraints["percentages"][element]["max"],
                            min(superior_elements),
                        ]
                    )

                    tmp_percentages[element]["min"] = min(
                        [
                            tmp_percentages[element]["min"],
                            tmp_percentages[element]["max"],
                        ]
                    )

            # if (
            #     len(
            #         self.constraints["percentages"][element][
            #             "inferior_elements"
            #         ]
            #     )
            #     > 0
            # ):
            #     inferior_elements = []
            #     for e in self.constraints["percentages"][element][
            #         "inferior_elements"
            #     ]:
            #         if e in self.composition:
            #             inferior_elements.append(self.composition[e])

            #     if len(inferior_elements) > 0:
            #         tmp_percentages[element]["min"] = max(
            #             [
            #                 self.constraints["percentages"][element]["min"],
            #                 max(inferior_elements),
            #             ]
            #         )

            #         tmp_percentages[element]["max"] = max(
            #             [
            #                 tmp_percentages[element]["min"],
            #                 tmp_percentages[element]["max"],
            #             ]
            #         )

        if lowest_precedence["element"] is not None:
            for element in self.composition:
                if element not in tmp_percentages:
                    tmp_percentages[element] = {
                        "max": lowest_precedence["percentage"],
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

        if self.constraints["max_elements"] == len(
            self.constraints["local_percentages"]
        ):
            total_max = 0
            for element in self.composition:
                if element in self.constraints["local_percentages"]:
                    total_max += self.constraints["local_percentages"][
                        element
                    ]["max"]
            while total_max < 1:
                for element in self.constraints["local_percentages"]:
                    if element not in self.composition:
                        value = min(
                            [
                                self.constraints["local_percentages"][element][
                                    "max"
                                ],
                                1 - total_max,
                            ]
                        )
                        self.composition.__setitem__(
                            element, value, respond_to_change=False
                        )
                        total_max += value

                if total_max < 1:
                    element_to_add = np.random.choice(
                        self.constraints["allowed_elements"], 1
                    )[0]
                    if element_to_add not in self.composition:
                        value = np.random.uniform()
                        self.composition.__setitem__(
                            element_to_add, value, respond_to_change=False
                        )
                        total_max += value

    def to_string(self) -> str:
        """Convert the alloy composition to a string

        :group: alloy.utils
        """

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
        """Convert alloy composition to string with LaTeX formatting of
        subscripts

        :group: alloy.utils
        """
        numbers = re.compile(r"(\d+)")
        return numbers.sub(r"$_{\1}$", self.to_string())

    def to_dict(self) -> dict:
        """Convert the alloy composition to a dictionary

        :group: alloy.utils
        """
        alloy_dict = {"composition": self.to_string()}
        return alloy_dict

    def round_composition(self):
        """Round elemental percentages in composition while maintaining sum

        :group: alloy.utils
        """

        if len(self.composition) == 0:
            return
        elif len(self.composition) == 1:
            self.composition[self.elements[0]] = 1.0

        digits = 4
        percentage_step = 0.0001
        if self.constraints is not None:
            if "digits" in self.constraints:
                digits = self.constraints["digits"]
            if "percentage_step" in self.constraints:
                percentage_step = self.constraints["percentage_step"]

        needs_rounding = False
        for element in self.elements:
            percentage_str = str(self.composition[element])
            length = len(percentage_str)
            if "." in percentage_str:
                length -= 2
            if length > digits:
                easy_round = False
                easy_rounders = ["0", "9"]
                count = Counter(percentage_str)
                for c in easy_rounders:
                    if c in count and not easy_round:
                        count[c] /= len(percentage_str)
                        if count[c] > 0.5:
                            easy_round = True
                            self.composition[element] = multiple_round(
                                self.composition[element],
                                percentage_step,
                                digits,
                            )
                if not easy_round:
                    needs_rounding = True
                    break

        if not needs_rounding:
            return

        integer_parts = []
        decimal_parts = []

        for element in self.elements:
            percentage = str(self.composition[element] * (10**digits))
            split_percentage = percentage.split(".")

            integer_parts.append(int(split_percentage[0]))

            if len(split_percentage) > 1:
                decimal_parts.append(
                    float(percentage) - float(split_percentage[0])
                )
            else:
                decimal_parts.append(0.0)

        undershoot = (10**digits) - sum(integer_parts)

        if undershoot > 0:
            if self.constraints is not None:

                precedence = {}
                for element in self.elements:
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
                filtered_precedence_order = self.elements

            i = 0
            while undershoot > 0:
                decimal_part_index = self.elements.index(
                    filtered_precedence_order[i]
                )

                constraints_violated = False
                if self.constraints is not None:
                    if (
                        filtered_precedence_order[i]
                        in self.constraints["local_percentages"]
                    ):
                        if decimal_part_index < len(integer_parts):

                            if (integer_parts[decimal_part_index] + 1) / (
                                10**digits
                            ) > self.constraints["local_percentages"][
                                filtered_precedence_order[i]
                            ][
                                "max"
                            ]:
                                constraints_violated = True

                if not constraints_violated:
                    if decimal_part_index < len(integer_parts):
                        integer_parts[decimal_part_index] += 1
                        undershoot -= 1
                else:
                    break
                i += 1

                if i >= len(filtered_precedence_order):
                    i = 0

            i = 0
            for element in self.elements:
                if i < len(integer_parts):
                    self.composition[element] = multiple_round(
                        integer_parts[i] / (10**digits),
                        percentage_step,
                        digits,
                    )
                else:
                    self.composition[element] = 0
                i += 1

        else:
            i = 0
            for element in self.elements:

                if i < len(integer_parts):
                    rounded_value = multiple_round(
                        integer_parts[i] / (10**digits),
                        percentage_step,
                        digits,
                    )

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
                else:
                    self.composition[element] = 0

                i += 1

        deviation = 1 - self.total_percentage
        abs_deviation = np.abs(deviation)
        if abs_deviation >= percentage_step:
            num_steps = int(abs_deviation // percentage_step)

            j = 0
            for _ in range(num_steps):
                step = percentage_step
                if deviation < 0:
                    step *= -1

                self.composition[self.elements[j]] += step
                if j > self.num_elements:
                    j = 0


def parse_composition(composition: Union[str, dict, Alloy]) -> dict:
    """Parse elemental percentages of an alloy from input

    :group: alloy.utils
    """
    if isinstance(composition, str):
        return parse_composition_string(composition)
    elif isinstance(composition, dict):
        return parse_composition_dict(composition)
    elif isinstance(composition, Alloy):
        return composition.composition


def parse_composition_string(composition_string: str) -> dict:
    """Parse elemental percentages of an alloy from a string

    :group: alloy.utils
    """

    if len(composition_string) == 0:
        return None

    if "(" in composition_string:

        sub_composition_percentage = (
            float(
                re.split(r"(\d+(?:\.\d+)?)", composition_string.split(")")[1])[
                    1
                ]
            )
            / 100.0
        )

        sub_composition_string = composition_string.split(")")[0].split("(")[1]

        sub_composition = parse_composition_string_block(
            sub_composition_string
        )
        for element in sub_composition:
            sub_composition[element] *= sub_composition_percentage

        pre_sub_composition_string = composition_string.split(")")[0].split(
            "("
        )[0]
        post_sub_composition_string = composition_string.split(")")[1].split(
            "("
        )[0]

        remaining_composition_string = ""
        if re.search("[a-zA-Z]", pre_sub_composition_string) is not None:
            remaining_composition_string += pre_sub_composition_string
        if re.search("[a-zA-Z]", post_sub_composition_string) is not None:
            remaining_composition_string += post_sub_composition_string

        remaining_composition = parse_composition_string_block(
            remaining_composition_string
        )

        composition = {**sub_composition, **remaining_composition}

    else:
        composition = parse_composition_string_block(composition_string)

    return filter_order_composition(composition)


def parse_composition_string_block(composition_string: str) -> dict:
    """Parse a block of a composition string, found between brackets, returning
    a composition dictionary for that block

    :group: alloy.utils
    """
    composition = {}

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

    return composition


def parse_composition_dict(composition: dict) -> dict:
    """Parse elemental percentages of an alloy from a dict

    :group: alloy.utils
    """

    if len(composition) == 0:
        return None

    needRescale = False
    for element in composition:
        if composition[element] > 1:
            needRescale = True
            break

    if needRescale:
        for element in composition:
            composition[element] /= 100.0

    return filter_order_composition(composition)


def filter_order_composition(composition: dict) -> OrderedDict:
    """Filter & order elements in an alloy composition

    Elements with percentage less than zero are filtered out.
    An OrderedDict is used to sort the composition in descending
    order of elemental percentage.

    :group: alloy.utils
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
    percentage_step: float = 0.01,
) -> dict:
    """Parse constraint rules from input

    :group: alloy.utils

    Parameters
    ----------
        min_elements
            Minimum number of elements in an alloy
        max_elements
            Maximum number of elements in an alloy
        percentages
            Dict of maximum and minimum percentages per element
        allowed_elements
            List of elements allowed in an alloy
        disallowed_elements
            List of elements not allowed in an alloy
        digits
            Number of significant figures to consider for percentages
        percentage_step
            Increment between percentages

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
        percentages[element]["inferior_elements"] = []
        for other_element in percentages:
            if element != other_element:
                if (
                    percentages[element]["precedence"]
                    < percentages[other_element]["precedence"]
                ):
                    percentages[element]["superior_elements"].append(
                        other_element
                    )
                elif (
                    percentages[element]["precedence"]
                    > percentages[other_element]["precedence"]
                ):
                    percentages[element]["inferior_elements"].append(
                        other_element
                    )

        if len(percentages[element]["superior_elements"]) > 0:
            inferior_min = percentages[element]["min"]
            for other_element in percentages:
                if (
                    other_element
                    not in percentages[element]["superior_elements"]
                ):
                    inferior_min = max(
                        [inferior_min, percentages[other_element]["min"]]
                    )
            if inferior_min < percentages[element]["max"]:
                percentages[element]["min"] = inferior_min

        if len(percentages[element]["inferior_elements"]) > 0:
            superior_min = percentages[element]["min"]
            for other_element in percentages[element]["inferior_elements"]:
                superior_min = max(
                    [superior_min, percentages[other_element]["min"]]
                )
            if superior_min > percentages[element]["min"]:
                percentages[element]["min"] = superior_min

    min_sum = sum([percentages[e]["min"] for e in percentages])
    if min_sum > 1:
        print(
            "Impossible constraints, mins for each element sum greater than 1"
        )

    for element in disallowed_elements:
        if element in allowed_elements:
            allowed_elements.remove(element)

    digits = len(str(percentage_step))
    if "." in str(percentage_step):
        digits -= 2

    return {
        "percentages": percentages,
        "local_percentages": percentages,
        "allowed_elements": allowed_elements,
        "min_elements": min_elements,
        "max_elements": max_elements,
        "digits": digits,
        "percentage_step": percentage_step,
    }


def donate_percentage(
    composition: Alloy.Composition,
    constraints: dict,
    donor: str,
    recipient: str,
):
    """Adjusts a composition by transferring some percentage from one element
    (the donor) to another element (the recipient).

    :group: alloy.utils

    Parameters
    ----------

    composition
        The percentages of the alloy.
    constraints
        The constraints on the alloy.
    donor
        The element to give away some percentage.
    recipient
        The element to recieve some percentage.

    """

    recipient_deficit = 0
    donor_surplus = 0

    if (
        recipient in constraints["local_percentages"]
        and recipient in composition
    ):
        recipient_deficit = (
            constraints["local_percentages"][recipient]["min"]
            - composition[recipient]
        )
    else:
        recipient_deficit = 0

    if donor in constraints["local_percentages"]:

        if composition[donor] > constraints["local_percentages"][donor]["max"]:
            donor_surplus = (
                composition[donor]
                - constraints["local_percentages"][donor]["max"]
            )
        elif (
            composition[donor] > constraints["local_percentages"][donor]["min"]
        ):
            donor_surplus = (
                composition[donor]
                - constraints["local_percentages"][donor]["min"]
            )
    else:
        donor_surplus = composition[donor]

    if normal_round(donor_surplus, constraints["digits"] + 1) > 0:
        if recipient_deficit <= 0 or recipient_deficit >= donor_surplus:
            donation = min([0.1, donor_surplus])
        else:
            donation = min([0.1, recipient_deficit])
        donation = normal_round(donation, constraints["digits"] + 1)
        # print(recipient, "gets", donation, "from", donor)
        composition[recipient] += donation
        composition[donor] -= donation
        # print(composition)
        # print()


def element_is_in_range(
    element: str,
    composition: Alloy.Composition,
    constraints: dict,
    direction: str,
    inclusive: bool = True,
) -> bool:
    """Returns True if an element is within its constrained percentage range,
    False if not.

    :group: alloy.utils

    Parameters
    ----------

    element
        The element to check the constraint range of.
    composition
        The percentages of the alloy.
    constraints
        The constraints on the alloy.
    direction
        Either "min" or "max" depending on which edge of the constraints are
        being checked.
    inclusive
        True if an element should be considered inside the range including
        the endpoint.

    """

    if element not in constraints["local_percentages"]:
        return True

    if element in composition:
        percentage = composition[element]
    else:
        percentage = 0

    if direction == "min":
        if inclusive:
            return (
                percentage
                >= constraints["local_percentages"][element][direction]
            )
        else:
            return (
                percentage
                > constraints["local_percentages"][element][direction]
            )

    elif direction == "max":
        if inclusive:
            return (
                percentage
                <= constraints["local_percentages"][element][direction]
            )

        else:
            return (
                percentage
                < constraints["local_percentages"][element][direction]
            )

    return False


def normal_round(num: float, ndigits: int = 0) -> float:
    """Rounds a float to the specified number of decimal places.

    :group: alloy.utils

    Parameters
    ----------
        num: the value to round
        ndigits: the number of digits to round to
    """
    if ndigits == 0:
        return int(num + 0.5)
    else:
        digit_value = 10**ndigits
        return int(num * digit_value + 0.5) / digit_value


def multiple_round(
    num: float, multiple: Union[float, int], digits=4
) -> Union[float, int]:
    """Round a number to the nearest multiple of another number.

    :group: alloy.utils

    Parameters
    ----------
    num
        Value to round
    multiple
        Multiple-of to round towards
    """
    return round(multiple * round(num / multiple), digits)
