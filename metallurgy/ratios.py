from typing import Union, List
from numbers import Number
from collections.abc import Iterable

import metallurgy as mg


def shell_valence_electron_concentration_ratio(
    alloy: Union[mg.Alloy, str, dict],
    period: Union[Number, None] = None,
    valence_electrons: Union[Number, None] = None,
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the ratio between shell number and valence electron concentration
    of an alloy.

    :group: calculations.ratios

    Parameters
    ----------

    alloy : mg.Alloy, str, dict
        The alloy for which to calculate the ratio.
    period : Number
        The effective period of the alloy.
    valence_electrons : Number
        The effective number of valence electrons of the alloy.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [shell_valence_electron_concentration_ratio(a) for a in alloy]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    if period is None:
        period = mg.linear_mixture(alloy, "period")
    if valence_electrons is None:
        valence_electrons = mg.linear_mixture(alloy, "valence_electrons")

    return period / valence_electrons


def shell_mendeleev_number_ratio(
    alloy: Union[mg.Alloy, str, dict],
    period: Union[Number, None] = None,
    mendeleev_number: Union[Number, None] = None,
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the ratio between shell number and Mendeleev number of an alloy.

    :group: calculations.ratios

    Parameters
    ----------

    alloy : mg.Alloy, str, dict
        The alloy for which to calculate the ratio.
    period : Number
        The effective period of the alloy.
    mendeleev_number : Number
        The effective Mendeleev number of the alloy.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [shell_mendeleev_number_ratio(a) for a in alloy]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    if period is None:
        period = mg.linear_mixture(alloy, "period")
    if mendeleev_number is None:
        mendeleev_number = mg.linear_mixture(
            alloy, "mendeleev_universal_sequence"
        )

    if period is None or mendeleev_number is None:
        return None

    return period / mendeleev_number
