import re
from collections import OrderedDict


class Alloy():
    def __init__(self, compositionString):
        self.compositionString = compositionString

        self.composition = parse_composition_string(self.compositionString)
        self.elements = self.composition.keys()


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
                split_element_percentage[1]) / 100.0) * major_composition_percentage

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

            decimal_places = 2
            if '.' in str(split_element_percentage[1]):
                decimal_places += len(
                    str(split_element_percentage[1]).split('.')[1])

            composition[split_element_percentage[0]] = round(
                float(split_element_percentage[1]) / 100.0, decimal_places)

    filtered_composition = {}
    for element in composition:
        if(composition[element] > 0):
            filtered_composition[element] = composition[element]

    ordered_composition = OrderedDict()
    elements = filtered_composition.keys()
    for element in sorted(elements):
        ordered_composition[element] = filtered_composition[element]

    return ordered_composition
