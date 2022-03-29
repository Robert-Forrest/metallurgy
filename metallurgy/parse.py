import re
from collections import OrderedDict


def parse_composition(composition):
    if isinstance(composition, str):
        return parse_composition_string(composition)
    elif isinstance(composition, dict):
        return parse_composition_dict(composition)


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

    needRescale = False
    for element in composition:
        if composition[element] > 1:
            needRescale = True
            break

    if needRescale:
        for element in composition:
            composition[element] /= 100.0

    return filter_order_composition(composition)


def filter_order_composition(composition):

    filtered_composition = {}
    for element in composition:
        if(composition[element] > 0):
            filtered_composition[element] = composition[element]

    ordered_composition = OrderedDict()
    elements = filtered_composition.keys()
    for element in sorted(elements):
        ordered_composition[element] = filtered_composition[element]

    return ordered_composition


def alloy_to_string(alloy):

    composition_str = ""
    for element in alloy.composition:
        percentage_str = str(alloy.composition[element] * 100.0)

        split_str = percentage_str.split('.')
        decimal = split_str[1]
        if decimal == '0':
            percentage_str = split_str[0]
        else:
            decimal_places = len(str(alloy.composition[element]).split('.')[1])
            percentage_str = str(round(float(percentage_str), decimal_places))

            split_str = percentage_str.split('.')
            decimal = split_str[1]
            if decimal == '0':
                percentage_str = split_str[0]

        composition_str += element + percentage_str

    return composition_str
