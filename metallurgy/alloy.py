import copy
import re
from collections import OrderedDict

import numpy as np
import elementy


class Alloy():
    class Composition(dict):

        def __init__(self, value, on_composition_change_callback, *args, **kwargs):
            super().__init__(value, *args, **kwargs)
            self.on_composition_change_callback = on_composition_change_callback

        def __setitem__(self, key, value):
            if value >= 0.01:
                super().__setitem__(key, value)
            else:
                if key in self.keys():
                    super().__delitem__(key)
            self.on_composition_change_callback()

    def __init__(self, composition, constraints=None):
        self.composition = parse_composition(composition)
        self.constraints = None

        self.clamp_composition()
        self.round_composition()

        if constraints is not None:
            self.constraints = parse_constraints(**constraints)

    @property
    def composition(self):
        return self._composition

    @composition.setter
    def composition(self, value):
        if isinstance(value, (dict, OrderedDict)):
            value = self.Composition(value, self.on_composition_change)
        self._composition = value

    def on_composition_change(self):
        self.determine_percentage_constraints()
        # self.rescale()

    @property
    def elements(self):
        return list(self.composition.keys())

    def rescale(self):

        if self.constraints is not None:
            self.apply_constraints()

        if (len(self.elements) == 1):
            for element in self.composition:
                self.composition[element] = 1.0

    def apply_constraints(self):

        constraints_applied = False
        while not self.constraints_satisfied():

            constraints_applied = True

            precedence = {}
            for element in self.constraints['local_percentages']:
                if self.constraints['local_percentages'][element]['min'] > 0:
                    if element not in self.composition:
                        self.composition[element] = 0.01

                precedence[element] = self.constraints['local_percentages'][element]['precedence']

            precedence_order = sorted(precedence, key=precedence.get, reverse=True)
            reverse_precedence_order = sorted(precedence, key=precedence.get)

            for element in precedence_order:
                if element not in self.composition:
                    if self.constraints['local_percentages'][element]['min'] > 0:
                        self.composition[element] = self.constraints['local_percentages'][element]['min']
                    else:
                        continue

                if self.composition[element] < self.constraints['local_percentages'][element]['min']:
                    for other_element in reverse_precedence_order:
                        if element != other_element and other_element in self.composition:

                            if self.composition[other_element] > \
                               self.constraints['local_percentages'][other_element]['max']:

                                element_deficit = self.constraints['local_percentages'][element]['min'] - \
                                    self.composition[element]

                                other_element_surplus = self.composition[other_element] - \
                                    self.constraints['local_percentages'][other_element]['max']

                                # print("A")
                                # print(self.composition)
                                # print(element, element_deficit)
                                # print(other_element, other_element_surplus)
                                # print()

                                if element_deficit >= other_element_surplus and other_element_surplus > 0:
                                    self.composition[element] += other_element_surplus
                                    self.composition[other_element] -= other_element_surplus
                                else:
                                    self.composition[element] += element_deficit
                                    self.composition[other_element] -= element_deficit

                                if element not in self.composition:
                                    break
                                if self.composition[element] >= \
                                   self.constraints['local_percentages'][element]['min']:

                                    break

                if element not in self.composition:
                    if self.constraints['local_percentages'][element]['min'] > 0:
                        self.composition[element] = \
                            self.constraints['local_percentages'][element]['min']
                    else:
                        continue

                if self.composition[element] < \
                   self.constraints['local_percentages'][element]['min']:

                    for other_element in sorted(
                            self.composition.keys(), key=lambda k: np.random.random()):

                        if other_element != element:

                            other_element_surplus = self.composition[other_element]
                            if other_element in self.constraints['local_percentages']:
                                if (self.constraints['local_percentages'][element]['precedence'] <
                                        self.constraints['local_percentages'][other_element]['precedence']):
                                    continue

                                other_element_surplus -= self.constraints['local_percentages'][other_element]['min']

                            if normal_round(other_element_surplus, self.constraints['sigfigs']+1) > 0:

                                element_deficit = self.constraints['local_percentages'][element]['min'] - \
                                    self.composition[element]

                                # print("B")
                                # print(self.composition)
                                # print(element, element_deficit)
                                # print(other_element, other_element_surplus)
                                # print()

                                if element_deficit >= self.composition[other_element]:
                                    self.composition[element] += other_element_surplus
                                    self.composition[other_element] -= other_element_surplus
                                else:
                                    self.composition[element] += element_deficit
                                    self.composition[other_element] -= element_deficit

                                if element not in self.composition:
                                    break
                                if self.composition[element] >= self.constraints['local_percentages'][element]['min']:
                                    break

                if element not in self.composition:
                    if self.constraints['local_percentages'][element]['min'] > 0:
                        self.composition[element] = self.constraints['local_percentages'][element]['min']
                    else:
                        continue

                if self.composition[element] > self.constraints['local_percentages'][element]['max']:
                    for other_element in reverse_precedence_order:
                        if element != other_element and other_element in self.composition:

                            if self.composition[other_element] < \
                               self.constraints['local_percentages'][other_element]['min']:
                                element_surplus = self.composition[element] - \
                                    self.constraints['local_percentages'][element]['max']

                                other_element_deficit = \
                                    self.constraints['local_percentages'][other_element]['min'] - \
                                    self.composition[other_element]

                                # print("C")
                                # print(self.composition)
                                # print(element, element_surplus)
                                # print(other_element, other_element_deficit)
                                # print()

                                if element_surplus >= other_element_deficit:
                                    self.composition[element] -= other_element_deficit
                                    self.composition[other_element] += element_surplus
                                else:
                                    self.composition[element] -= element_surplus
                                    self.composition[other_element] += element_surplus

                                if element not in self.composition:
                                    break
                                if self.composition[element] <= \
                                   self.constraints['local_percentages'][element]['max']:
                                    break

                if element not in self.composition:
                    if self.constraints['local_percentages'][element]['min'] > 0:
                        self.composition[element] = self.constraints['local_percentages'][element]['min']
                    else:
                        continue

                if self.composition[element] > self.constraints['local_percentages'][element]['max']:
                    for other_element in sorted(self.composition.keys(), key=lambda k: np.random.random()):
                        if other_element != element:

                            if other_element in self.constraints['local_percentages']:
                                other_element_deficit = self.constraints['local_percentages'][other_element]['max'] - \
                                    self.composition[other_element]
                            else:
                                other_element_deficit = 1.0 - \
                                    self.composition[other_element]

                            element_surplus = self.composition[element] - \
                                self.constraints['local_percentages'][element]['max']

                            element_surplus = np.max(
                                [element_surplus, self.constraints['percentage_step']])
                            other_element_deficit = np.max(
                                [other_element_deficit, self.constraints['percentage_step']])

                            # print("D")
                            # print(self.composition)
                            # print(element, element_surplus)
                            # print(other_element, other_element_deficit)
                            # print()

                            if element_surplus >= other_element_deficit and other_element_deficit > 0:
                                self.composition[element] -= other_element_deficit
                                self.composition[other_element] += other_element_deficit
                            else:
                                self.composition[element] -= element_surplus
                                self.composition[other_element] += element_surplus

                            if element not in self.composition:
                                break
                            if self.composition[element] <= self.constraints['local_percentages'][element]['max']:
                                break

            if (len(self.composition) > self.constraints['max_elements']):

                excess = len(self.composition) - self.constraints['max_elements']

                toDelete = []
                ordered_elements = sorted(self.composition, key=self.composition.get)
                for element in ordered_elements:
                    if element in self.constraints['local_percentages']:
                        if self.constraints['local_percentages'][element]['min'] == 0:
                            toDelete.append(element)
                    else:
                        toDelete.append(element)

                    if len(toDelete) == excess:
                        break

                for element in toDelete:
                    del self.composition[element]

            elif (len(self.composition) < self.constraints['min_elements']):

                while len(self.composition) < self.constraints['min_elements']:

                    element_to_add = np.random.choice(
                        self.constraints['allowed_elements'], 1)[0]
                    if element_to_add not in self.composition:
                        percentage = np.random.uniform()
                        self.composition[element_to_add] = percentage

            self.clamp_composition()

        if not constraints_applied:
            self.clamp_composition()
        self.round_composition()

    def constraints_satisfied(self):
        satisfied = True

        if self.constraints is not None:

            discrepancy = np.abs(
                1-multiple_round(sum(self.composition.values()), self.constraints['percentage_step']))
            if discrepancy > self.constraints['percentage_step']:
                # print("Sum != 1", sum(self.composition.values()), discrepancy)
                # print(self.composition)
                # print()
                satisfied = False

            if satisfied:
                for element in self.constraints['local_percentages']:
                    if element in self.composition:
                        if self.composition[element] < self.constraints['local_percentages'][element]['min']:
                            # print("element below min", element,
                            #       self.composition[element], self.constraints['local_percentages'][element]['min'])
                            # print(self.composition)
                            # print()
                            satisfied = False
                            break
                        elif self.composition[element] > self.constraints['local_percentages'][element]['max']:
                            # print("element above max", element,
                            #       self.composition[element], self.constraints['local_percentages'][element]['max'])
                            # print(self.composition)
                            # print()
                            satisfied = False
                            break
                    elif self.constraints['local_percentages'][element]['min'] > 0.0:
                        # print("element missing", element,
                        #       self.constraints['local_percentages'][element]['min'])
                        # print(self.composition)
                        # print()
                        satisfied = False
                        break

            if satisfied:
                if len(self.composition) > self.constraints['max_elements']:
                    satisfied = False
                    # print("too many elements")
                    # print(self.composition)
                    # print()
                elif len(self.composition) < self.constraints['min_elements']:
                    satisfied = False
                    # print("too few elements")
                    # print(self.composition)
                    # print()

        return satisfied

    def clamp_composition(self):

        total_percentage = sum(self.composition.values())

        for element in self.elements:
            self.composition[element] /= total_percentage

    def determine_percentage_constraints(self):

        if self.constraints is None:
            return

        tmp_percentages = copy.deepcopy(self.constraints['percentages'])

        lowest_precedence = {'element': None, 'precedence': np.Inf, 'percentage': np.Inf}
        for element in self.constraints['percentages']:
            if element in self.composition:
                if (self.constraints['percentages'][element]['precedence'] <= lowest_precedence['precedence']
                    and self.constraints['percentages'][element]['precedence'] > 0
                        and self.composition[element] < lowest_precedence['percentage']):

                    lowest_precedence['precedence'] = self.constraints['percentages'][element]['precedence']
                    lowest_precedence['element'] = element
                    lowest_precedence['percentage'] = self.composition[element]

            if len(self.constraints['percentages'][element]['superior_elements']) > 0:
                superior_elements = []
                for e in self.constraints['percentages'][element]['superior_elements']:
                    if e in self.composition:
                        superior_elements.append(self.composition[e])
                if len(superior_elements) > 0:
                    tmp_percentages[element]['max'] = min(superior_elements)
                else:
                    tmp_percentages[element]['max'] = 0

        if lowest_precedence['element'] is not None:
            for element in self.composition:
                if element not in tmp_percentages:
                    maxPercent = lowest_precedence['percentage']

                    tmp_percentages[element] = {
                        'max': maxPercent,
                        'min': 0,
                        'precedence': 0,
                        'superior_elements': []
                    }

                    for other_element in tmp_percentages:
                        if element != other_element:
                            if (tmp_percentages[element]['precedence']
                                    < tmp_percentages[other_element]['precedence']):
                                tmp_percentages[element]['superior_elements'].append(
                                    other_element)

        self.constraints['local_percentages'] = tmp_percentages

    def to_string(self):
        composition_str = ""
        for element in self.elements:
            percentage_str = str(self.composition[element] * 100.0)

            split_str = percentage_str.split('.')
            decimal = split_str[1]
            if decimal == '0':
                percentage_str = split_str[0]
            else:
                decimal_places = len(str(self.composition[element]).split('.')[1])
                percentage_str = str(round(float(percentage_str), decimal_places))

                split_str = percentage_str.split('.')
                decimal = split_str[1]
                if decimal == '0':
                    percentage_str = split_str[0]

            composition_str += element + percentage_str

        return composition_str

    def to_pretty_string(self):
        numbers = re.compile(r'(\d+)')
        return numbers.sub(r'$_{\1}$', self.to_string())

    def round_composition(self):
        if(len(self.composition) == 0):
            return

        if self.constraints is not None:
            sigfigs = self.constraints['sigfigs']
            percentage_step = self.constraints['percentage_step']
        else:
            sigfigs = 2
            percentage_step = 0.01

        integer_parts = []
        decimal_parts = []

        elements = list(self.composition.keys())
        for element in elements:

            rounded_percentage = normal_round(
                self.composition[element], sigfigs)

            if rounded_percentage > 0:

                percentage = str(self.composition[element] *
                                 (10**sigfigs))
                split_percentage = percentage.split('.')

                integer_parts.append(int(split_percentage[0]))

                if(len(split_percentage) > 1):
                    decimal_parts.append(float(percentage)-float(split_percentage[0]))
                else:
                    decimal_parts.append(0.0)

        undershoot = (10**sigfigs)-sum(integer_parts)

        if(undershoot > 0):
            if self.constraints is not None:

                precedence = {}
                for element in elements:
                    if element in self.constraints['percentages']:
                        precedence[element] = self.constraints['percentages'][element]['precedence']
                    else:
                        precedence[element] = 0
                precedence_order = sorted(precedence, key=precedence.get, reverse=True)

                filtered_precedence_order = []
                for element in precedence_order:
                    if element in self.composition:
                        filtered_precedence_order.append(element)
            else:
                filtered_precedence_order = list(self.composition.keys())

            i = 0
            while(undershoot > 0):
                decimal_part_index = list(
                    self.composition.keys()).index(filtered_precedence_order[i])

                constraints_violated = False
                if self.constraints is not None:
                    if filtered_precedence_order[i] in self.constraints['percentages']:
                        if ((integer_parts[decimal_part_index] + 1)/(10**sigfigs)
                                > self.constraints['percentages'][filtered_precedence_order[i]]['max']):
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
                    integer_parts[i] / (10**sigfigs), sigfigs)
                i += 1

        else:
            elements = list(self.composition.keys())
            for element in elements:
                self.composition[element] = normal_round(multiple_round(
                    self.composition[element], percentage_step), sigfigs)


def parse_composition(composition):
    if isinstance(composition, str):
        return parse_composition_string(composition)
    elif isinstance(composition, dict):
        return parse_composition_dict(composition)
    elif isinstance(composition, Alloy):
        return composition.composition


def parse_composition_string(composition_string):

    composition = {}
    if('(' in composition_string):
        major_composition = composition_string.split(')')[0].split('(')[1]

        major_composition_percentage = float(re.split(
            r'(\d+(?:\.\d+)?)', composition_string.split(')')[1])[1]) / 100.0

        split_major_composition = re.findall(
            r'[A-Z][^A-Z]*', major_composition)

        for element_percentage in split_major_composition:
            split_element_percentage = re.split(
                r'(\d+(?:\.\d+)?)', element_percentage)
            composition[split_element_percentage[0]] = (float(
                split_element_percentage[1]) / 100.0) * \
                major_composition_percentage

        minor_composition = composition_string.split(
            ')')[1][len(str(int(major_composition_percentage * 100))):]
        split_minor_composition = re.findall(
            r'[A-Z][^A-Z]*', minor_composition)
        for element_percentage in split_minor_composition:
            split_element_percentage = re.split(
                r'(\d+(?:\.\d+)?)', element_percentage)

            decimal_places = 2
            if '.' in str(split_element_percentage[1]):
                decimal_places += len(
                    str(split_element_percentage[1]).split('.')[1])

            composition[split_element_percentage[0]] = round(
                float(split_element_percentage[1]) / 100.0, decimal_places)

    else:

        split_composition = re.findall(
            r'[A-Z][^A-Z]*', composition_string)

        for element_percentage in split_composition:
            split_element_percentage = re.split(
                r'(\d+(?:\.\d+)?)', element_percentage)

            if(len(split_element_percentage) > 1):
                decimal_places = 2
                if '.' in str(split_element_percentage[1]):
                    decimal_places += len(
                        str(split_element_percentage[1]).split('.')[1])

                composition[split_element_percentage[0]] = round(
                    float(split_element_percentage[1]) / 100.0, decimal_places)
            else:
                composition[split_element_percentage[0]] = 1.0 / \
                    len(split_composition)

    return filter_order_composition(composition)


def parse_composition_dict(composition):
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


def filter_order_composition(composition):

    filtered_composition = {}
    for element in composition:
        if(composition[element] > 0):
            filtered_composition[element] = composition[element]

    ordered_composition = OrderedDict()
    for element in sorted(filtered_composition, key=filtered_composition.get, reverse=True):
        ordered_composition[element] = filtered_composition[element]

    return ordered_composition


def parse_constraints(
        min_elements=1,
        max_elements=10,
        percentages={},
        allowed_elements=[e.symbol for e in elementy.PeriodicTable().elements],
        sigfigs=3,
        percentage_step=0.01):

    if not isinstance(percentages, dict):
        if isinstance(percentages, list):
            tmp_percentages = {}
            for element in percentages:
                tmp_percentages[element] = {}
            percentages = tmp_percentages

    for element in percentages:
        if 'min' not in percentages[element]:
            percentages[element]['min'] = 0.0
        else:
            percentages[element]['min'] = max(
                percentages[element]['min'], 0.0)

        if 'max' not in percentages[element]:
            percentages[element]['max'] = 1.0
        else:
            percentages[element]['max'] = min(
                percentages[element]['max'], 1.0)

        if 'precedence' not in percentages[element]:
            percentages[element]['precedence'] = 0

    for element in percentages:
        percentages[element]['superior_elements'] = []
        for other_element in percentages:
            if element != other_element:
                if percentages[element]['precedence'] < percentages[other_element]['precedence']:
                    percentages[element]['superior_elements'].append(
                        other_element)

    min_sum = sum([percentages[e]['min'] for e in percentages])
    # max_sum = sum([percentages[e]['max'] for e in percentages])

    if min_sum > 1:
        print("Impossible constraints, mins for each element sum greater than 1")

    return {
        'percentages': percentages,
        'local_percentages': percentages,
        'allowed_elements': allowed_elements,
        'min_elements': min_elements,
        'max_elements': max_elements,
        'sigfigs': sigfigs,
        'percentage_step': percentage_step
    }


def normal_round(num, ndigits=0):
    """
    Rounds a float to the specified number of decimal places.
    num: the value to round
    ndigits: the number of digits to round to
    """
    if ndigits == 0:
        return int(num + 0.5)
    else:
        digit_value = 10 ** ndigits
        return int(num * digit_value + 0.5) / digit_value


def multiple_round(num, multiple):
    return multiple * round(num/multiple)
