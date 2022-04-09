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

    seriesA = mg.periodic_table.elements[elementA]['series']
    if(elementA == 'Ca' or elementA == 'Sr' or elementA == 'Ba'):
        seriesA = 'non_transition_metal'

    seriesB = mg.periodic_table.elements[elementB]['series']
    if(elementB == 'Ca' or elementB == 'Sr' or elementB == 'Ba'):
        seriesB = 'non_transition_metal'

    if seriesA == 'transition_metal' and seriesB == 'transition_metal':
        P = 14.1
        R = 0
    elif seriesA != 'transition_metal' and seriesB != 'transition_metal':
        P = 10.6
        R = 0
    else:
        P = 12.3
        R = mg.periodic_table.elements[elementA]['miedema_R'] * \
            mg.periodic_table.elements[elementB]['miedema_R']

    Q = P * 9.4

    return Q, P, R


def calculate_electronegativity_enthalpy_component(elementA, elementB, P):
    electronegativityDiff = mg.periodic_table.elements[elementA]['electronegativity_miedema'] \
        - mg.periodic_table.elements[elementB]['electronegativity_miedema']
    return -P * (electronegativityDiff**2)


def calculate_WS_enthalpy_component(elementA, elementB, Q):
    return Q * (wigner_seitz_electron_density_discontinuity_delta(
        elementA, elementB)**2)


def wigner_seitz_electron_density_discontinuity_delta(elementA, elementB):
    densityA = mg.periodic_table.elements[elementA]['wigner_seitz_electron_density']
    densityB = mg.periodic_table.elements[elementB]['wigner_seitz_electron_density']
    return (densityA**(1. / 3.)) - (densityB**(1. / 3.))


def calculate_surface_concentration(elements, volumes, composition):

    reduced_vol_A = composition[elements[0]] * (volumes[0]**(2.0 / 3.0))
    reduced_vol_B = composition[elements[1]] * (volumes[1]**(2.0 / 3.0))

    return reduced_vol_A / (reduced_vol_A + reduced_vol_B)


def calculate_corrected_volume(elementA, elementB, Cs_A):

    pureV = mg.periodic_table.elements[elementA]['volume_miedema']

    electronegativityDiff = mg.periodic_table.elements[elementA]['electronegativity_miedema'] \
        - mg.periodic_table.elements[elementB]['electronegativity_miedema']

    a = None
    if(elementA in ['Ca', 'Sr', 'Ba']):
        a = 0.04
    elif(elementA in ['Ru', 'Rh', 'Pd', 'Os', 'Ir', 'Pt', 'Au']):
        a = 0.07

    if a is None:
        if(mg.periodic_table.elements[elementA]['series'] == 'alkaliMetal'):
            a = 0.14
        elif(mg.periodic_table.elements[elementA]['valence_electrons'] == 2):
            a = 0.1
        elif(mg.periodic_table.elements[elementA]['valence_electrons'] == 3):
            a = 0.07
        else:
            a = 0.04

    f_AB = 1 - Cs_A

    correctedV = (pureV**(2.0 / 3.0)) * (1 + a * f_AB * electronegativityDiff)

    return correctedV


def calculate_interface_enthalpy(elementA, elementB, volumeA):

    densityA = mg.periodic_table.elements[elementA]['wigner_seitz_electron_density']
    densityB = mg.periodic_table.elements[elementB]['wigner_seitz_electron_density']

    return 2 * volumeA * Gamma(elementA, elementB) / \
        (densityA**(-1. / 3.) + densityB**(-1. / 3.))


def calculate_topological_enthalpy(composition):
    topological_enthalpy = 0
    for element in composition:
        topological_enthalpy += mg.periodic_table.elements[element]['fusion_enthalpy'] * \
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
            V_A_alloy = mg.periodic_table.elements[pair[0]]['volume_miedema']
            V_B_alloy = mg.periodic_table.elements[pair[1]]['volume_miedema']

            if V_A_alloy is None or V_B_alloy is None:
                return None

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


def mixing_Gibbs_free_energy(alloy):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_Gibbs_free_energy(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    H = mixing_enthalpy(alloy)
    Tm = linear_mixture(alloy, "melting_temperature")
    S = entropy.mixing_entropy(alloy)

    if H is None or Tm is None or S is None:
        return None
    return (H * 1e3) - Tm * S * constants.idealGasConstant


def mismatch_PHS(alloy):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mismatch_PHS(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    H = mixing_enthalpy(alloy)
    S = entropy.mismatch_entropy(alloy)

    if H is not None and S is not None:
        return H * S
    else:
        return None


def mixing_PHS(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_PHS(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    H = mixing_enthalpy(alloy)
    S = entropy.mixing_entropy(alloy)

    if H is not None and S is not None:
        return H * S
    else:
        return None


def mixing_PHSS(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_PHSS(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    H = mixing_enthalpy(alloy)
    Smix = entropy.mixing_entropy(alloy)
    Smismatch = entropy.mismatch_entropy(alloy)

    if H is None or Smix is None or Smismatch is None:
        return None
    else:
        return H*Smix*Smismatch


def thermodynamic_factor(alloy):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [thermodynamic_factor(a) for a in list(alloy)]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    Tm = linear_mixture(alloy, 'melting_temperature')
    H = mixing_enthalpy(alloy)
    S = entropy.mixing_entropy(alloy)

    if Tm is None or H is None or S is None:
        return None

    return (Tm * S) / (np.abs(H * 1e3) + 1e-10)
