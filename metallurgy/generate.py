import copy
import random

import numpy as np
import elementy

from .alloy import Alloy


def random_alloy(
        min_elements=1,
        max_elements=10,
        required_elements=[],
        allowed_elements=[e for e in elementy.PeriodicTable().elements]):

    requirements = parse_requirements(
        min_elements,
        max_elements,
        required_elements,
        allowed_elements)

    if min_elements < max_elements:
        num_alloy_elements = np.random.randint(
            min_elements, max_elements)
    else:
        num_alloy_elements = max_elements
    num_alloy_elements -= len(requirements['elements'])

    if num_alloy_elements > 0:
        other_elements = requirements['allowed_elements'][:]
        for element in requirements['elements'].keys():
            other_elements.remove(element)
        elements = list(requirements['elements'].keys(
        )) + list(np.random.choice(other_elements, num_alloy_elements, replace=False))

    else:
        elements = list(np.random.choice(
            list(requirements['elements'].keys()),
            num_alloy_elements + len(requirements['elements']),
            replace=False))

    percentages = list(np.random.dirichlet(np.ones(len(elements)), size=1)[0])

    composition = {}
    for j in range(len(elements)):
        composition[elements[j]] = percentages[j]

    composition = rescale(composition, requirements)
    if composition is None:
        return random_alloy(
            min_elements=min_elements,
            max_elements=max_elements,
            required_elements=requirements['elements'],
            allowed_elements=requirements['allowed_elements'])

    return Alloy(composition)


def random_alloys(num_alloys,
                  min_elements=1,
                  max_elements=10,
                  required_elements=[],
                  allowed_elements=[e for e in elementy.PeriodicTable().elements]):

    return [random_alloy(min_elements, max_elements, required_elements, allowed_elements) for _ in range(num_alloys)]


def rescale(alloy, requirements=None):

    total_percentage = sum(alloy.composition.values())

    if total_percentage > 0:

        alloy = apply_requirements(alloy, requirements)

        if(len(alloy.composition) == 0):
            return None

    else:
        return None

    if (len(alloy.composition) == 1):
        for element in alloy.composition:
            alloy.composition[element] = 1.0

    return alloy


def apply_requirements(alloy, requirements=None):

    if requirements is not None:
        requirements['elements'] = determine_element_requirements(
            alloy.composition, requirements)

    constraints_applied = False
    while not constraints_satisfied(alloy.composition, requirements):

        constraints_applied = True
        if(len(alloy.composition) == 1):
            composition = {}
            break

        precedence = {}
        for element in requirements['elements']:
            if requirements['elements'][element]['min'] > 0:
                if element not in alloy.composition:
                    alloy.composition[element] = 0
            precedence[element] = requirements['elements'][element]['precedence']

        precedence_order = sorted(precedence, key=precedence.get, reverse=True)
        reverse_precedence_order = sorted(precedence, key=precedence.get)

        requirements['elements'] = determine_element_requirements(
            composition, requirements)

        for element in precedence_order:
            if element not in alloy.composition:
                continue
            if alloy.composition[element] < requirements['elements'][element]['min']:
                for other_element in reverse_precedence_order:
                    if element != other_element and other_element in alloy.composition:
                        requirements['elements'] = determine_element_requirements(
                            alloy.composition, requirements)

                        if alloy.composition[other_element] > requirements['elements'][other_element]['max']:
                            element_deficit = requirements['elements'][element]['min'] - \
                                alloy.composition[element]
                            other_element_surplus = alloy.composition[other_element] - \
                                requirements['elements'][other_element]['max']

                            # print("A")
                            # print(element, element_deficit)
                            # print(other_element, other_element_surplus)
                            # print()

                            if element_deficit >= other_element_surplus and other_element_surplus > 0:
                                alloy.composition[element] += other_element_surplus
                                alloy.composition[other_element] -= other_element_surplus
                            else:
                                alloy.composition[element] += element_deficit
                                alloy.composition[other_element] -= element_deficit

                            if alloy.composition[element] >= requirements['elements'][element]['min']:
                                break

            if alloy.composition[element] < requirements['elements'][element]['min']:
                for other_element in sorted(alloy.composition.keys(), key=lambda k: random.random()):
                    if other_element != element:
                        requirements['elements'] = determine_element_requirements(
                            alloy.composition, requirements)

                        other_element_surplus = alloy.composition[other_element]
                        if other_element in requirements['elements']:
                            if (requirements['elements'][element]['precedence'] <
                                    requirements['elements'][other_element]['precedence']):
                                continue

                            other_element_surplus -= requirements['elements'][other_element]['min']

                        if normal_round(other_element_surplus, requirements['sigfigs']+1) > 0:

                            element_deficit = requirements['elements'][element]['min'] - \
                                alloy.composition[element]

                            # print("B")
                            # print(element, element_deficit)
                            # print(other_element, other_element_surplus)
                            # print()

                            if element_deficit >= alloy.composition[other_element]:
                                alloy.composition[element] += other_element_surplus
                                alloy.composition[other_element] -= other_element_surplus
                            else:
                                alloy.composition[element] += element_deficit
                                alloy.composition[other_element] -= element_deficit

                            if alloy.composition[element] >= requirements['elements'][element]['min']:
                                break

            if alloy.composition[element] > requirements['elements'][element]['max']:
                for other_element in reverse_precedence_order:
                    if element != other_element and other_element in alloy.composition:
                        requirements['elements'] = determine_element_requirements(
                            alloy.composition, requirements)

                        if alloy.composition[other_element] < requirements['elements'][other_element]['min']:
                            element_surplus = alloy.composition[element] - \
                                requirements['elements'][element]['max']

                            other_element_deficit = requirements['elements'][other_element]['min'] - \
                                alloy.composition[other_element]

                            # print("C")
                            # print(element, element_surplus)
                            # print(other_element, other_element_deficit)
                            # print()

                            if element_surplus >= other_element_deficit:
                                alloy.composition[element] -= other_element_deficit
                                alloy.composition[other_element] += element_surplus
                            else:
                                alloy.composition[element] -= element_surplus
                                alloy.composition[other_element] += element_surplus

                            if alloy.composition[element] <= requirements['elements'][element]['max']:
                                break

            if alloy.composition[element] > requirements['elements'][element]['max']:
                for other_element in sorted(alloy.composition.keys(), key=lambda k: random.random()):
                    if other_element != element:
                        requirements['elements'] = determine_element_requirements(
                            alloy.composition, requirements)

                        if other_element in requirements['elements']:
                            other_element_deficit = requirements['elements'][other_element]['max'] - \
                                alloy.composition[other_element]
                        else:
                            other_element_deficit = 1.0 - \
                                alloy.composition[other_element]

                        element_surplus = alloy.composition[element] - \
                            requirements['elements'][element]['max']

                        element_surplus = np.max(
                            [element_surplus, requirements['percentage_step']])
                        other_element_deficit = np.max(
                            [other_element_deficit, requirements['percentage_step']])

                        # print("D")
                        # print(element, element_surplus)
                        # print(other_element, other_element_deficit)
                        # print()

                        if element_surplus >= other_element_deficit and other_element_deficit > 0:
                            alloy.composition[element] -= other_element_deficit
                            alloy.composition[other_element] += other_element_deficit
                        else:
                            alloy.composition[element] -= element_surplus
                            alloy.composition[other_element] += element_surplus

                        if alloy.composition[element] <= requirements['elements'][element]['max']:
                            break

        if (len(alloy.composition) > requirements['max_elements']):

            excess = len(alloy.composition) - requirements['max_elements']

            requirements['elements'] = determine_element_requirements(
                alloy.composition, requirements)

            toDelete = []
            ordered_elements = sorted(alloy.composition, key=alloy.composition.get)
            for element in ordered_elements:
                if element in requirements['elements']:
                    if requirements['elements'][element]['min'] == 0:
                        toDelete.append(element)
                else:
                    toDelete.append(element)

                if len(toDelete) == excess:
                    break

            for element in toDelete:
                del alloy.composition[element]

        elif (len(alloy.composition) < requirements['min_elements']):

            requirements['elements'] = determine_element_requirements(
                alloy.composition, requirements)

            while len(alloy.composition) < requirements['min_elements']:

                element_to_add = np.random.choice(
                    requirements['allowed_elements'], 1)[0]
                if element_to_add not in alloy.composition:
                    percentage = np.random.uniform()
                    alloy.composition[element_to_add] = percentage

        alloy.composition = clamp_composition(alloy.composition)

    if not constraints_applied:
        composition = clamp_composition(alloy.composition)
    alloy.composition = round_composition(alloy.composition, requirements)

    return alloy


def constraints_satisfied(composition, requirements=None):
    satisfied = True

    if requirements is not None:
        requirements['elements'] = determine_element_requirements(composition, requirements)

        discrepancy = np.abs(
            1-multiple_round(sum(composition.values()), requirements['percentage_step']))
        if discrepancy > requirements['percentage_step']:
            # print("Sum != 1", sum(composition.values()), discrepancy)
            # print(composition)
            # print()
            satisfied = False

        if satisfied:
            for element in requirements['elements']:
                if element in composition:
                    if composition[element] < requirements['elements'][element]['min']:
                        # print("element below min", element,
                        #       composition[element], requirements['elements'][element]['min'])
                        # print(composition)
                        # print()
                        satisfied = False
                        break
                    elif composition[element] > requirements['elements'][element]['max']:
                        # print("element above max", element,
                        #       composition[element], requirements['elements'][element]['max'])
                        # print(composition)
                        # print()
                        satisfied = False
                        break
                elif requirements['elements'][element]['min'] > 0.0:
                    # print("element missing", element,
                    #       requirements['elements'][element]['min'])
                    # print(composition)
                    # print()
                    satisfied = False
                    break

        if satisfied:
            if len(composition) > requirements['max_elements']:
                satisfied = False
                # print("too many elements")
                # print(composition)
                # print()
            elif len(composition) < requirements['min_elements']:
                satisfied = False
                # print("too few elements")
                # print(composition)
                # print()
    
    return satisfied


def round_composition(composition, requirements=None):
    if(len(composition) == 0):
        return composition

    if requirements is not None:
        sigfigs = requirements['sigfigs']
        percentage_step = requirements['sigfigs']
    else:
        sigfigs = 2
        percentage_step = 0.01

    integer_parts = []
    decimal_parts = []
    toDelete = []
    for element in composition:
        rounded_percentage = normal_round(
            composition[element], sigfigs)
        # rounded_percentage = normal_round(multiple_round(
        #     composition[element], percentage_step), sigfigs)
        if rounded_percentage > 0:

            percentage = str(composition[element] *
                             (10**sigfigs))
            split_percentage = percentage.split('.')

            integer_parts.append(int(split_percentage[0]))

            if(len(split_percentage) > 1):
                decimal_parts.append(float(split_percentage[1]))
            else:
                decimal_parts.append(0.0)

        elif element in composition:
            toDelete.append(element)

    for element in toDelete:
        del composition[element]

    undershoot = (10**sigfigs)-sum(integer_parts)

    if(undershoot > 0):
        if requirements is not None:
            requirements['elements'] = determine_element_requirements(
                composition, requirements)

            precedence = {}
            for element in composition:
                if element in requirements['elements']:
                    precedence[element] = requirements['elements'][element]['precedence']
                else:
                    precedence[element] = 0
            precedence_order = sorted(precedence, key=precedence.get, reverse=True)

            filtered_precedence_order = []
            for element in precedence_order:
                if element in composition:
                    filtered_precedence_order.append(element)
        else:
            filtered_precedence_order = list(composition.keys())
                    
        i = 0
        while(undershoot > 0):
            decimal_part_index = list(
                composition.keys()).index(filtered_precedence_order[i])

            constraints_violated = False
            if requirements is not None:
                if filtered_precedence_order[i] in requirements['elements']:
                   if ((integer_parts[decimal_part_index] + 1)/(10**sigfigs)
                           > requirements['elements'][filtered_precedence_order[i]]['max']):
                       constraints_violated = True

            if not constraints_violated:
                integer_parts[decimal_part_index] += 1
                undershoot -= 1
            i += 1

            if i >= len(filtered_precedence_order):
                i = 0

        i = 0
        for element in composition:
            composition[element] = normal_round(
                integer_parts[i] / (10**sigfigs), sigfigs)
            i += 1

    else:
        for element in composition:
            composition[element] = normal_round(multiple_round(
                composition[element], percentage_step), sigfigs)
            # composition[element] = normal_round(
            #     composition[element], sigfigs)

    return composition


def clamp_composition(composition):
    for element in composition:
        if composition[element] < 0:
            composition[element] = 0

    total_percentage = sum(composition.values())
    # # if normal_round(total_percentage, requirements['sigfigs']) != 1.0:
    # if multiple_round(total_percentage, percentage_step) != 1.0:
    for element in composition:
        composition[element] = composition[element] / total_percentage

    return composition


def determine_element_requirements(composition, requirements):
    tmp_required_elements = copy.deepcopy(requirements['elements'])

    lowest_precedence = {'element': None, 'precedence': np.Inf, 'percentage': np.Inf}
    for element in requirements['elements']:
        if element in composition:
            if (requirements['elements'][element]['precedence'] <= lowest_precedence['precedence']
                and requirements['elements'][element]['precedence'] > 0
                    and composition[element] < lowest_precedence['percentage']):

                lowest_precedence['precedence'] = requirements['elements'][element]['precedence']
                lowest_precedence['element'] = element
                lowest_precedence['percentage'] = composition[element]

        if len(requirements['elements'][element]['superior_elements']) > 0:
            superior_elements = []
            for e in requirements['elements'][element]['superior_elements']:
                if e in composition:
                    superior_elements.append(composition[e])
            if len(superior_elements) > 0:
                tmp_required_elements['elements'][element]['max'] = min(superior_elements)
            else:
                tmp_required_elements['elements'][element]['max'] = 0

    if lowest_precedence['element'] is not None:
        for element in composition:
            if element not in tmp_required_elements['elements']:
                # if lowest_precedence['element'] in composition:
                #     maxPercent = composition[lowest_precedence['element']]
                # else:
                #     maxPercent = 0
                maxPercent = lowest_precedence['percentage']

                tmp_required_elements['elements'][element] = {
                    'max': maxPercent,
                    'min': 0,
                    'precedence': 0,
                    'superior_elements': []
                }

                for other_element in tmp_required_elements['elements']:
                    if element != other_element:
                        if (tmp_required_elements['elements'][element]['precedence']
                                < tmp_required_elements['elements'][other_element]['precedence']):
                            tmp_required_elements['elements'][element]['superior_elements'].append(
                                other_element)

    return tmp_required_elements


def parse_requirements(
        min_elements,
        max_elements,
        required_elements,
        allowed_elements,
        sigfigs=3,
        percentage_step=0.01):

    if not isinstance(required_elements, dict):
        if isinstance(required_elements, list):
            tmp_required_elements = {}
            for element in required_elements:
                tmp_required_elements[element] = {}
            required_elements = tmp_required_elements

    for element in required_elements:
        if 'min' not in required_elements[element]:
            required_elements[element]['min'] = 0.0
        else:
            required_elements[element]['min'] = max(
                required_elements[element]['min'], 0.0)

        if 'max' not in required_elements[element]:
            required_elements[element]['max'] = 1.0
        else:
            required_elements[element]['max'] = min(
                required_elements[element]['max'], 1.0)

        if 'precedence' not in required_elements[element]:
            required_elements[element]['precedence'] = 0

    for element in required_elements:
        required_elements[element]['superior_elements'] = []
        for other_element in required_elements:
            if element != other_element:
                if required_elements[element]['precedence'] < required_elements[other_element]['precedence']:
                    required_elements[element]['superior_elements'].append(
                        other_element)

    min_sum = sum([required_elements[e]['min'] for e in required_elements])
    # max_sum = sum([required_elements[e]['max'] for e in required_elements])

    if min_sum > 1:
        print("Impossible constraints, mins for each element sum greater than 1")

    return {
        'elements': required_elements,
        'allowed_elements': allowed_elements,
        'min_elements': min_elements,
        'max_elements': max_elements,
        'sigfigs': sigfigs,
        'percentage_step': percentage_step
    }


def multiple_round(num, multiple):
    return multiple * round(num/multiple)


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
