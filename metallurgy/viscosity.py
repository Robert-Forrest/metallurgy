from typing import Union, List
from numbers import Number
from collections.abc import Iterable

import numpy as np

import metallurgy as mg


def viscosity(
    alloy: Union[mg.Alloy, str, dict],
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the approximate viscosity of an alloy.

    :group: calculations.viscosity

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the viscosity.

    """
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [viscosity(a) for a in alloy]
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    const = 3.077e-3
    elementalViscosity = {}
    for element in alloy.elements:
        mass = mg.periodic_table.elements[element]["mass"]
        Tm = mg.periodic_table.elements[element]["melting_temperature"]
        molar_volume = mg.periodic_table.elements[element]["molar_volume"]
        if mass is None or Tm is None or molar_volume is None:
            return None

        elementalViscosity[element] = (
            const * np.sqrt((mass / 1000) * Tm) / (molar_volume * 1.0e-6)
        )

    sum_aG = 0
    for element in alloy.elements:
        mass = mg.periodic_table.elements[element]["mass"]
        density = mg.periodic_table.elements[element]["density"]
        Tm = mg.periodic_table.elements[element]["melting_temperature"]
        if mass is None or density is None or Tm is None:
            return None

        sum_aG += (
            Tm
            * alloy.composition[element]
            * np.log(
                (elementalViscosity[element] * (mass / 1000))
                / (
                    mg.constants.plankConstant
                    * mg.constants.avogadroNumber
                    * (density)
                    * 1000
                )
            )
        )

    sum_aG *= mg.constants.idealGasConstant

    averageMolarVolume = 0
    for element in alloy.elements:
        averageMolarVolume += alloy.composition[element] * (
            mg.periodic_table.elements[element]["molar_volume"] * 1.0e-6
        )

    H = mg.enthalpy.mixing_enthalpy(alloy)
    if H is None:
        return None

    return (
        (mg.constants.plankConstant * mg.constants.avogadroNumber)
        / (averageMolarVolume)
    ) * np.exp(
        (sum_aG - 0.155 * H)
        / (
            mg.constants.idealGasConstant
            * mg.linear_mixture(alloy, "melting_temperature")
        )
    )
