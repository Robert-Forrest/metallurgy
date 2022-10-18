"""``metallurgy.enthalpy``
=============================

Module providing enthalpy related calculations.

"""

from collections.abc import Iterable
from numbers import Number
from typing import Tuple, Union, List

import numpy as np

import metallurgy as mg


def Gamma(element_a: str, element_b: str) -> Union[Number, None]:
    """Calculates the gamma term of the Miedema model.
    See equation 1 of: http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations

    Parameters
    ----------

    element_a : str
        The periodic table symbol of element A
    element_a : str
        The periodic table symbol of element B
    """

    Q, P, R = calculate_QPR(element_a, element_b)
    if R is not None:
        return (
            calculate_electronegativity_enthalpy_component(
                element_a, element_b, P
            )
            + calculate_WS_enthalpy_component(element_a, element_b, Q)
            - R
        )
    else:
        return None


def calculate_QPR(
    element_a: str, element_b: str
) -> Union[Tuple[Number, Number, Number], None]:
    """Calculates the Q, P, and R factors of the Miedema model.
    See equation 1 of: http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations

    Parameters
    ----------

    element_a : str
        The periodic table symbol of element A
    element_a : str
        The periodic table symbol of element B
    """

    series_a = mg.periodic_table.elements[element_a]["series"]
    if element_a in ("Ca", "Sr", "Ba"):
        series_a = "non_transition_metal"

    series_b = mg.periodic_table.elements[element_b]["series"]
    if element_b in ("Ca", "Sr", "Ba"):
        series_b = "non_transition_metal"

    if series_a == "transition_metal" and series_b == "transition_metal":
        P = 14.1
        R = 0
    elif series_a != "transition_metal" and series_b != "transition_metal":
        P = 10.6
        R = 0
    else:
        P = 12.3

        if (
            mg.periodic_table.elements[element_a]["miedema_R"] is not None
            and mg.periodic_table.elements[element_b]["miedema_R"] is not None
        ):
            R = (
                mg.periodic_table.elements[element_a]["miedema_R"]
                * mg.periodic_table.elements[element_b]["miedema_R"]
            )
        else:
            R = None

    Q = P * 9.4

    return Q, P, R


def calculate_electronegativity_enthalpy_component(
    element_a: str, element_b: str, P: Number
) -> Number:
    """Calculates the electronegativity contribution to the gamma factor in the
    Miedema model of mixing enthalpy.  See equation 1 of:
    http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations

    Parameters
    ----------

    element_a : str
        The periodic table symbol of element A
    element_a : str
        The periodic table symbol of element B
    P : Number
        An empirical factor dependent on the kinds of elements being
        mixed. P=14.1 for two transition metals, P=10.7 for two non-transition
        metals, and P=12.35 for one of each kind.
    """

    electronegativityDiff = (
        mg.periodic_table.elements[element_a]["electronegativity_miedema"]
        - mg.periodic_table.elements[element_b]["electronegativity_miedema"]
    )
    return -P * (electronegativityDiff**2)


def calculate_WS_enthalpy_component(
    element_a: str, element_b: str, Q: Number
) -> Number:
    """Calculates the Wigner-Seitz radius discontinuity contribution to the
    gamma factor in the Miedema model of mixing enthalpy.  See equation 1 of:
    http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations

    Parameters
    ----------

    element_a : str
        The periodic table symbol of element A
    element_b : str
        The periodic table symbol of element B
    Q : Number
        An empirical factor dependent on the kinds of elements being
        mixed. Dependent on the P factor discussed, Q = 9.4*P, discussed in
        documentation of
        :func:`~metallurgy.enthalpy.calculate_electronegativity_enthalpy_component`.
    """

    return Q * (
        wigner_seitz_electron_density_discontinuity_delta(element_a, element_b)
        ** 2
    )


def wigner_seitz_electron_density_discontinuity_delta(
    element_a: str, element_b: str
) -> Number:
    """Calculates the Wigner-Seitz radius discontinuity contribution to the
    gamma factor in the Miedema model of mixing enthalpy.  See equation 1 of:
    http://dx.doi.org/10.1016/j.cpc.2016.08.013

    Parameters
    ----------

    element_a : str
        The periodic table symbol of element A
    element_a : str
        The periodic table symbol of element B
    """

    density_a = mg.periodic_table.elements[element_a][
        "wigner_seitz_electron_density"
    ]
    density_b = mg.periodic_table.elements[element_b][
        "wigner_seitz_electron_density"
    ]
    return (density_a ** (1.0 / 3.0)) - (density_b ** (1.0 / 3.0))


def calculate_surface_concentration(
    elements: List[str], volumes: List[Number], composition: dict
) -> Number:
    """Calculates the surface concentration in the Miedema model of mixing
    enthalpy.  See equation 2 of: http://dx.doi.org/10.1016/j.cpc.2016.08.013

    Parameters
    ----------

    elements : List[str]
        The elements being used to calculate the surface concentration.
    volumes : List[Number]
        The atomic volumes of the elements.
    composition : dict
       Dictionary containing the percentage of each element in the surface composition.
    """

    reduced_vol_A = composition[elements[0]] * (volumes[0] ** (2.0 / 3.0))
    reduced_vol_B = composition[elements[1]] * (volumes[1] ** (2.0 / 3.0))

    return reduced_vol_A / (reduced_vol_A + reduced_vol_B)


def calculate_corrected_volume(
    element_a: str, element_b: str, surface_concentration_a: Number
):
    """Calculates the corrected volume of element_a in an alloy with element_b,
    as defined by the Meidema model.  See equation 2 of:
    http://dx.doi.org/10.1016/j.cpc.2016.08.013

    Parameters
    ----------

    element_a : str
        The element for which to correct the volume.
    element_b : str
        The other element in the alloy.
    surface_concentration_a : Number
        The surface concentration of element_a, as calculated by:
        :func:`~metallurgy.enthalpy.calculate_surface_concentration`.
    """

    pureV = mg.periodic_table.elements[element_a]["volume_miedema"]

    electronegativityDiff = (
        mg.periodic_table.elements[element_a]["electronegativity_miedema"]
        - mg.periodic_table.elements[element_b]["electronegativity_miedema"]
    )

    a = None
    if element_a in ["Ca", "Sr", "Ba"]:
        a = 0.04
    elif element_a in ["Ru", "Rh", "Pd", "Os", "Ir", "Pt", "Au"]:
        a = 0.07

    if a is None:
        if mg.periodic_table.elements[element_a]["series"] == "alkaliMetal":
            a = 0.14
        elif mg.periodic_table.elements[element_a]["valence_electrons"] == 2:
            a = 0.1
        elif mg.periodic_table.elements[element_a]["valence_electrons"] == 3:
            a = 0.07
        else:
            a = 0.04

    f_AB = 1 - surface_concentration_a

    correctedV = (pureV ** (2.0 / 3.0)) * (
        1 + a * f_AB * electronegativityDiff
    )

    return correctedV


def calculate_interface_enthalpy(element_a, element_b, volumeA):

    density_a = mg.periodic_table.elements[element_a][
        "wigner_seitz_electron_density"
    ]
    density_b = mg.periodic_table.elements[element_b][
        "wigner_seitz_electron_density"
    ]

    gamma = Gamma(element_a, element_b)
    if gamma is not None:
        return (
            2
            * volumeA
            * gamma
            / (density_a ** (-1.0 / 3.0) + density_b ** (-1.0 / 3.0))
        )


def calculate_topological_enthalpy(composition):
    topological_enthalpy = 0
    for element in composition:
        topological_enthalpy += (
            mg.periodic_table.elements[element]["fusion_enthalpy"]
            * composition[element]
        )

    return topological_enthalpy


def mixing_enthalpy(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_enthalpy(a) for a in list(alloy)]
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    if len(alloy.elements) > 1:

        elementPairs = [
            (a, b)
            for idx, a in enumerate(alloy.elements)
            for b in alloy.elements[idx + 1 :]
        ]

        total_mixing_enthalpy = 0
        for pair in elementPairs:
            tmpComposition = {}
            subComposition = 0
            for element in pair:
                subComposition += alloy.composition[element]
            for element in pair:
                tmpComposition[element] = (
                    alloy.composition[element] / subComposition
                )

            surface_concentration_a = None
            V_A_alloy = mg.periodic_table.elements[pair[0]]["volume_miedema"]
            V_B_alloy = mg.periodic_table.elements[pair[1]]["volume_miedema"]

            if V_A_alloy is None or V_B_alloy is None:
                return None

            for _ in range(10):

                surface_concentration_a = calculate_surface_concentration(
                    pair, [V_A_alloy, V_B_alloy], tmpComposition
                )

                V_A_alloy = calculate_corrected_volume(
                    pair[0], pair[1], surface_concentration_a
                )

                V_B_alloy = calculate_corrected_volume(
                    pair[1], pair[0], 1 - surface_concentration_a
                )

            interface_AB = calculate_interface_enthalpy(
                pair[0], pair[1], V_A_alloy
            )
            interface_BA = calculate_interface_enthalpy(
                pair[1], pair[0], V_B_alloy
            )

            if interface_AB is not None and interface_BA is not None:

                chemical_enthalpy = (
                    alloy.composition[pair[0]]
                    * alloy.composition[pair[1]]
                    * (
                        (1 - surface_concentration_a) * interface_AB
                        + surface_concentration_a * interface_BA
                    )
                )
                total_mixing_enthalpy += chemical_enthalpy

            else:
                return None

    else:
        total_mixing_enthalpy = 0.0

    return total_mixing_enthalpy


def mixing_Gibbs_free_energy(alloy):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_Gibbs_free_energy(a) for a in list(alloy)]
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    H = mixing_enthalpy(alloy)
    Tm = mg.linear_mixture(alloy, "melting_temperature")
    S = mg.entropy.mixing_entropy(alloy)

    if H is None or Tm is None or S is None:
        return None
    return (H * 1e3) - Tm * S * mg.constants.idealGasConstant


def mismatch_PHS(alloy):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mismatch_PHS(a) for a in list(alloy)]
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    H = mixing_enthalpy(alloy)
    S = mg.entropy.mismatch_entropy(alloy)

    if H is not None and S is not None:
        return H * S
    else:
        return None


def mixing_PHS(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_PHS(a) for a in list(alloy)]
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    H = mixing_enthalpy(alloy)
    S = mg.entropy.mixing_entropy(alloy)

    if H is not None and S is not None:
        return H * S
    else:
        return None


def mixing_PHSS(alloy):
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_PHSS(a) for a in list(alloy)]
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    H = mixing_enthalpy(alloy)
    Smix = mg.entropy.mixing_entropy(alloy)
    Smismatch = mg.entropy.mismatch_entropy(alloy)

    if H is None or Smix is None or Smismatch is None:
        return None
    else:
        return H * Smix * Smismatch


def thermodynamic_factor(alloy):

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [thermodynamic_factor(a) for a in list(alloy)]
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    Tm = mg.linear_mixture(alloy, "melting_temperature")
    H = mixing_enthalpy(alloy)
    S = mg.entropy.mixing_entropy(alloy)

    if Tm is None or H is None or S is None:
        return None

    return (Tm * S) / (np.abs(H * 1e3) + 1e-10)
