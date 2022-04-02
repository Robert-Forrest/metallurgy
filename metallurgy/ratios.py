from collections.abc import Iterable

from . import linear_mixture
from .alloy import Alloy


def shell_to_valence_electron_concentration(alloy, period=None, valence_electrons=None):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [shell_to_valence_electron_concentration(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if period is None:
        period = linear_mixture(alloy, 'period')
    if valence_electrons is None:
        valence_electrons = linear_mixture(alloy, 'valence_electrons')

    return period / valence_electrons


def shell_to_mendeleev_number(alloy, period=None, mendeleev=None):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [shell_to_mendeleev_number(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if period is None:
        period = linear_mixture(alloy, 'period')
    if mendeleev is None:
        mendeleev = linear_mixture(alloy, 'mendeleev_universal_sequence')

    return period / mendeleev
