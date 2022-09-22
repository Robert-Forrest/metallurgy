from collections.abc import Iterable

import metallurgy as mg
from . import linear_mixture
from .alloy import Alloy


def valence_proportion(alloy, orbital):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [valence_proportion(a, orbital) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    total_valence = linear_mixture(alloy, "valence_electrons")

    orbitalCount = {}
    for element in alloy.elements:
        orbitalCount[element] = 0

        valence_electrons = mg.periodic_table.elements[element][
            "valence_electrons"
        ]
        orbitals = mg.periodic_table.elements[element]["orbitals"]

        i = 0
        electrons = 0
        while electrons < valence_electrons:
            electrons += orbitals[-1 - i]["electrons"]
            if orbitals[-1 - i]["orbital"][-1] == orbital:
                orbitalCount[element] += orbitals[-1 - i]["electrons"]
            i += 1

    if total_valence > 0:
        total = 0
        for element in alloy.elements:
            total += orbitalCount[element] * alloy.composition[element]
        return total / total_valence

    else:
        return 0


def s_valence(alloy):
    return valence_proportion(alloy, "s")


def p_valence(alloy):
    return valence_proportion(alloy, "p")


def d_valence(alloy):
    return valence_proportion(alloy, "d")


def f_valence(alloy):
    return valence_proportion(alloy, "f")
