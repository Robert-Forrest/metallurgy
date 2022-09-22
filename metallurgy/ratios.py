from collections.abc import Iterable

from . import linear_mixture
from .alloy import Alloy


def shell_valence_electron_concentration_ratio(
    alloy, period=None, valence_electrons=None
):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [shell_valence_electron_concentration_ratio(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if period is None:
        period = linear_mixture(alloy, "period")
    if valence_electrons is None:
        valence_electrons = linear_mixture(alloy, "valence_electrons")

    return period / valence_electrons


def shell_mendeleev_number_ratio(alloy, period=None, mendeleev=None):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [shell_mendeleev_number_ratio(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if period is None:
        period = linear_mixture(alloy, "period")
    if mendeleev is None:
        mendeleev = linear_mixture(alloy, "mendeleev_universal_sequence")

    if period is None or mendeleev is None:
        return None
    return period / mendeleev
