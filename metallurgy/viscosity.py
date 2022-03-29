import numpy as np
import metallurgy as mg
from . import enthalpy
from . import linear_mixture
from . import constants
from .alloy import Alloy


def calculate_molar_volume(element):
    return mg.periodic_table.dict[element]['mass'] / mg.periodic_table.dict[element]['density']


def calculate_viscosity(alloy, mixing_enthalpy=None):
    if not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    const = 3.077e-3
    elementalViscosity = {}
    for element in alloy.elements:
        elementalViscosity[element] = const * np.sqrt(
            (mg.periodic_table.dict[element]['mass'] / 1000) *
            mg.periodic_table.dict[element]['melting_temperature']) / \
            (calculate_molar_volume(element) * 1.0E-6)

    sum_aG = 0
    for element in alloy.elements:
        sum_aG += mg.periodic_table.dict[element]['melting_temperature'] * \
            alloy.composition[element] * np.log((elementalViscosity[element] * (
                mg.periodic_table.dict[element]['mass'] / 1000)) / (
                constants.plankConstant * constants.avogadroNumber * (
                    mg.periodic_table.dict[element]['density']) * 1000))

    sum_aG *= constants.idealGasConstant

    averageMolarVolume = 0
    for element in alloy.elements:
        averageMolarVolume += alloy.composition[element] * \
            (calculate_molar_volume(element) * 1.0E-6)

    if mixing_enthalpy is None:
        mixing_enthalpy = enthalpy.calculate_mixing_enthalpy(alloy)

    viscosity = ((constants.plankConstant * constants.avogadroNumber) /
                 (averageMolarVolume)) * \
        np.exp((sum_aG - 0.155 * mixing_enthalpy) /
               (constants.idealGasConstant *
                linear_mixture(alloy, 'melting_temperature')))

    return viscosity
