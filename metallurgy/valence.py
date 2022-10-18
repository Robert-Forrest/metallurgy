"""Valence related calculations"""

from typing import Union, List
from collections.abc import Iterable
from numbers import Number

import metallurgy as mg


def valence_proportion(
    alloy: Union[mg.Alloy, str, dict], orbital: str
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the proportion of the valence electrons which are in a particular
    orbital.

    :group: calculations.valence

    Parameters
    ----------

    alloy : mg.Alloy, str, dict
        The alloy for which to calculate the valence proportion.

    orbital : str
        The orbital to calculate the proportion of.
    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [valence_proportion(a, orbital) for a in alloy]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    total_valence = mg.linear_mixture(alloy, "valence_electrons")

    orbital_count = {}
    for element in alloy.elements:
        orbital_count[element] = 0

        valence_electrons = mg.periodic_table.elements[element][
            "valence_electrons"
        ]
        orbitals = mg.periodic_table.elements[element]["orbitals"]

        i = 0
        electrons = 0
        while electrons < valence_electrons:
            electrons += orbitals[-1 - i]["electrons"]
            if orbitals[-1 - i]["orbital"][-1] == orbital:
                orbital_count[element] += orbitals[-1 - i]["electrons"]
            i += 1

    if total_valence > 0:
        total = 0
        for element in alloy.elements:
            total += orbital_count[element] * alloy.composition[element]
        return total / total_valence

    return 0


def s_valence(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the proportion of the valence electrons which are in the s
    orbital.

    :group: calculations.valence

    Parameters
    ----------

    alloy : mg.Alloy, str, dict
        The alloy for which to calculate the s-valence proportion.

    """
    return valence_proportion(alloy, "s")


def p_valence(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the proportion of the valence electrons which are in the p
    orbital.

    :group: calculations.valence

    Parameters
    ----------

    alloy : mg.Alloy, str, dict
        The alloy for which to calculate the p-valence proportion.

    """
    return valence_proportion(alloy, "p")


def d_valence(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the proportion of the valence electrons which are in the d
    orbital.

    :group: calculations.valence

    Parameters
    ----------

    alloy : mg.Alloy, str, dict
        The alloy for which to calculate the d-valence proportion.

    """
    return valence_proportion(alloy, "d")


def f_valence(
    alloy: Union[mg.Alloy, str, dict]
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the proportion of the valence electrons which are in the f
    orbital.

    :group: calculations.valence

    Parameters
    ----------

    alloy : mg.Alloy, str, dict
        The alloy for which to calculate the f-valence proportion.

    """
    return valence_proportion(alloy, "f")
