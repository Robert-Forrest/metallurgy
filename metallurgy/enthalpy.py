from collections.abc import Iterable

import numpy as np

import metallurgy as mg
from .alloy import Alloy
from . import linear_mixture
from . import constants
from . import entropy


def Gamma(elementA, elementB):
    Q, P, R = calculate_QPR(elementA, elementB)
    return calculate_electronegativity_enthalpy_component(
        elementA, elementB, P) + \
        calculate_WS_enthalpy_component(elementA, elementB, Q) - R


def calculate_QPR(elementA, elementB):

    seriesA = mg.periodic_table.data[elementA]['series']
    if(elementA == 'Ca' or elementA == 'Sr' or elementA == 'Ba'):
        seriesA = 'nonTransitionMetal'

    seriesB = mg.periodic_table.data[elementB]['series']
    if(elementB == 'Ca' or elementB == 'Sr' or elementB == 'Ba'):
        seriesB = 'nonTransitionMetal'

    if seriesA == 'transitionMetal' and seriesB == 'transitionMetal':
        P = 14.1
        R = 0
    elif seriesA != 'transitionMetal' and seriesB != 'transitionMetal':
        P = 10.6
        R = 0
    else:
        P = 12.3
        R = mg.periodic_table.data[elementA]['miedema_R'] * \
            mg.periodic_table.data[elementB]['miedema_R']

    Q = P * 9.4

    return Q, P, R


def calculate_electronegativity_enthalpy_component(elementA, elementB, P):
    electronegativityDiff = mg.periodic_table.data[elementA]['electronegativity_miedema'] \
        - mg.periodic_table.data[elementB]['electronegativity_miedema']

    return -P * (electronegativityDiff**2)


def calculate_WS_enthalpy_component(elementA, elementB, Q):
    return Q * (diffDiscontinuity(elementA, elementB)**2)


def diffDiscontinuity(elementA, elementB):
    densityA = mg.periodic_table.data[elementA]['wigner_seitz_electron_density']
    densityB = mg.periodic_table.data[elementB]['wigner_seitz_electron_density']
    return (densityA**(1. / 3.)) - (densityB**(1. / 3.))


def calculate_surface_concentration(elements, volumes, composition):

    reduced_vol_A = composition[elements[0]] * (volumes[0]**(2.0 / 3.0))
    reduced_vol_B = composition[elements[1]] * (volumes[1]**(2.0 / 3.0))

    return reduced_vol_A / (reduced_vol_A + reduced_vol_B)


def calculate_corrected_volume(elementA, elementB, Cs_A):

    pureV = mg.periodic_table.data[elementA]['volume_miedema']

    electronegativityDiff = mg.periodic_table.data[elementA]['electronegativity_miedema'] \
        - mg.periodic_table.data[elementB]['electronegativity_miedema']

    a = None
    if(elementA in ['Ca', 'Sr', 'Ba']):
        a = 0.04
    elif(elementA in ['Ru', 'Rh', 'Pd', 'Os', 'Ir', 'Pt', 'Au']):
        a = 0.07

    if a is None:
        if(mg.periodic_table.data[elementA]['series'] == 'alkaliMetal'):
            a = 0.14
        elif(mg.periodic_table.data[elementA]['valence_electrons'] == 2):
            a = 0.1
        elif(mg.periodic_table.data[elementA]['valence_electrons'] == 3):
            a = 0.07
        else:
            a = 0.04

    f_AB = 1 - Cs_A

    correctedV = (pureV**(2.0 / 3.0)) * (1 + a * f_AB * electronegativityDiff)

    return correctedV


def calculate_interface_enthalpy(elementA, elementB, volumeA):

    densityA = mg.periodic_table.data[elementA]['wigner_seitz_electron_density']
    densityB = mg.periodic_table.data[elementB]['wigner_seitz_electron_density']

    return 2 * volumeA * Gamma(elementA, elementB) / \
        (densityA**(-1. / 3.) + densityB**(-1. / 3.))


def calculate_topological_enthalpy(composition):
    topological_enthalpy = 0
    for element in composition:
        topological_enthalpy += mg.periodic_table.data[element]['fusion_enthalpy'] * \
            composition[element]

    return topological_enthalpy


def mixing_enthalpy(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_enthalpy(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if(len(alloy.elements) > 1):

        elementPairs = [(a, b) for idx, a in enumerate(alloy.elements)
                        for b in alloy.elements[idx + 1:]]

        total_mixing_enthalpy = 0
        for pair in elementPairs:
            tmpComposition = {}
            subComposition = 0
            for element in pair:
                subComposition += alloy.composition[element]
            for element in pair:
                tmpComposition[element] = alloy.composition[element] / \
                    subComposition

            Cs_A = None
            V_A_alloy = mg.periodic_table.data[pair[0]]['volume_miedema']
            V_B_alloy = mg.periodic_table.data[pair[1]]['volume_miedema']

            for _ in range(10):

                Cs_A = calculate_surface_concentration(
                    pair, [V_A_alloy, V_B_alloy], tmpComposition)

                V_A_alloy = calculate_corrected_volume(
                    pair[0], pair[1], Cs_A)

                V_B_alloy = calculate_corrected_volume(
                    pair[1], pair[0], 1 - Cs_A)

            chemical_enthalpy = alloy.composition[pair[0]] * \
                alloy.composition[pair[1]] * (
                    (1 - Cs_A) *
                    calculate_interface_enthalpy(pair[0], pair[1], V_A_alloy) +
                    Cs_A *
                    calculate_interface_enthalpy(pair[1], pair[0], V_B_alloy)
            )

            total_mixing_enthalpy += chemical_enthalpy

    else:
        total_mixing_enthalpy = 0

    return total_mixing_enthalpy


def mixing_Gibbs_free_energy(alloy, mixing_enthalpy=None,
                             melting_temperature=None,
                             mixing_entropy=None):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_Gibbs_free_energy(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if mixing_enthalpy is None:
        mixing_enthalpy = mixing_enthalpy(alloy)
    if melting_temperature is None:
        melting_temperature = linear_mixture(alloy, "melting_temperature")
    if mixing_entropy is None:
        mixing_entropy = entropy.mixing_entropy(alloy)

    return (mixing_enthalpy * 1e3) - melting_temperature * \
        mixing_entropy * constants.idealGasConstant


def mismatch_PHS(alloy, mixing_enthalpy=None, mismatch_entropy=None):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mismatch_PHS(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if mixing_enthalpy is None:
        mixing_enthalpy = mixing_enthalpy(alloy)
    if mismatch_entropy is None:
        mismatch_entropy = entropy.mismatch_entropy(alloy)

    return mixing_enthalpy * mismatch_entropy


def mixing_PHS(alloy, mixing_enthalpy=None, mixing_entropy=None):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_PHS(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if mixing_enthalpy is None:
        mixing_enthalpy = mixing_enthalpy(alloy)
    if mixing_entropy is None:
        mixing_entropy = entropy.mixing_entropy(alloy)

    return mixing_enthalpy * mixing_entropy


def mixing_PHSS(alloy, mixing_enthalpy=None, mixing_entropy=None, mismatch_entropy=None):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_PHSS(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if mixing_enthalpy is None:
        mixing_enthalpy = mixing_enthalpy(alloy)
    if mixing_entropy is None:
        mixing_entropy = entropy.mixing_entropy(alloy)
    if mismatch_entropy is None:
        mismatch_entropy = entropy.mismatch_entropy(alloy)

    return mixing_enthalpy * mixing_entropy * mismatch_entropy


def thermodynamic_factor(alloy, melting_temperature=None, mixing_enthalpy=None, mixing_entropy=None):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [thermodynamic_factor(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if melting_temperature is None:
        melting_temperature = linear_mixture(alloy, 'melting_temperature')
    if mixing_enthalpy is None:
        mixing_enthalpy = mixing_enthalpy(alloy)
    if mixing_entropy is None:
        mixing_entropy = entropy.mixing_entropy(alloy)

    return (melting_temperature * mixing_entropy) / (np.abs(mixing_enthalpy * 1e3) + 1e-10)
