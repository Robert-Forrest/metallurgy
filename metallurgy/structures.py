import numpy as np
import metallurgy as mg
from .alloy import Alloy


def calculate_structure_mismatch(alloy):
    if isinstance(alloy, list):
        return [calculate_structure_mismatch(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    structures = {}
    for element in alloy.elements:
        if(mg.periodic_table.data[element]['phase'] == 'solid'):
            structure = mg.periodic_table.data[element]['crystal_structure']
        else:
            structure = mg.periodic_table.data[element]['phase']

        if structure not in structures:
            structures[structure] = 0
        structures[structure] += alloy.composition[element]

    if(len(structures) > 1):
        shannonEntropy = 0
        for structure in structures:
            shannonEntropy -= structures[structure] * \
                np.log(structures[structure])
        return shannonEntropy
    else:
        return 0
