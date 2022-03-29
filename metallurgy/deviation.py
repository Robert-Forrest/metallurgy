import numpy as np
from pandas.api.types import is_numeric_dtype
import metallurgy as mg
from .alloy import Alloy


def deviation(alloy, feature_name):

    if not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    data = mg.periodic_table.dict

    if(len(alloy.elements) > 1):

        if(isinstance(data[alloy.elements[0]][feature_name], (int, float, list))):

            mean = 0
            for element in alloy.elements:
                value = data[element][feature_name]
                if value is None:
                    return None

                if(isinstance(value, list)):
                    value = value[0]

                mean += alloy.composition[element] * value

            deviation = 0
            for element in alloy.elements:
                value = data[element][feature_name]

                if(isinstance(value, list)):
                    value = value[0]

                deviation += alloy.composition[element] * \
                    ((value - mean)**2)

            return deviation**0.5

        else:
            values = {}
            for element in alloy.elements:
                value = data[element][feature_name]
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
