import numbers
from collections.abc import Iterable

import numpy as np
import metallurgy as mg

from .alloy import Alloy


def deviation(alloy, feature_name):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [deviation(a, feature_name) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if(len(alloy.elements) > 1):

        if(isinstance(mg.periodic_table.elements[alloy.elements[0]][feature_name], (int, float, list))):

            mean = 0
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][feature_name]
                if value is None:
                    return None

                if(isinstance(value, list)):
                    value = value[0]
                if(not isinstance(value, numbers.Number)):
                    return None

                mean += alloy.composition[element] * value

            total_deviation = 0
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][feature_name]

                if(isinstance(value, list)):
                    value = value[0]
                if(not isinstance(value, numbers.Number)):
                    return None

                total_deviation += alloy.composition[element] * \
                    ((value - mean)**2)

            return total_deviation**0.5

        else:
            values = {}
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][feature_name]
                if value is None:
                    return None

                if value not in values:
                    values[value] = 0
                values[value] += alloy.composition[element]

            if(len(values) > 1):
                shannonEntropy = 0
                for value in values:
                    shannonEntropy -= values[value] * \
                        np.log(values[value])
                return shannonEntropy
            else:
                return 0

    else:
        return 0
