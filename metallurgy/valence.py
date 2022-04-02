from collections.abc import Iterable

import metallurgy as mg
from . import linear_mixture
from .alloy import Alloy


def calculate_valence_proportion(alloy, orbital):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [calculate_valence_proportion(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    totalValence = linear_mixture(alloy, 'valence_electrons')

    orbitalCount = {}
    for element in alloy.elements:
        orbitalCount[element] = 0

        valence_electrons = mg.periodic_table.data[element]['valence_electrons']
        orbitals = mg.periodic_table.data[element]['orbitals']

        i = 0
        electrons = 0
        while electrons < valence_electrons:
            electrons += orbitals[-1 - i]['electrons']
            if orbitals[-1 - i]['orbital'][-1] == orbital:
                orbitalCount[element] += orbitals[-1 - i]['electrons']
            i += 1

    total = 0
    for element in alloy.elements:
        total += orbitalCount[element] * alloy.composition[element]

    return total / totalValence
