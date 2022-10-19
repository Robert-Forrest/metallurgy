"""Module providing enthalpy related calculations."""

from collections.abc import Iterable
from numbers import Number
from typing import Tuple, Union, List

import numpy as np

import metallurgy as mg


def gamma(element_a: str, element_b: str) -> Union[Number, None]:
    """Calculates the gamma term of the Miedema model.
    See equation 1 of: http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations.enthalpy

    Parameters
    ----------

    element_a
        The periodic table symbol of element A
    element_b
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

    return None


def calculate_QPR(
    element_a: str, element_b: str
) -> Union[Tuple[Number, Number, Number], None]:
    """Calculates the Q, P, and R factors of the Miedema model.
    See equation 1 of: http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations.enthalpy

    Parameters
    ----------

    element_a
        The periodic table symbol of element A
    element_b
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

    :group: calculations.enthalpy

    Parameters
    ----------

    element_a
        The periodic table symbol of element A
    element_b
        The periodic table symbol of element B
    P
        An empirical factor dependent on the kinds of elements being
        mixed. P=14.1 for two transition metals, P=10.7 for two non-transition
        metals, and P=12.35 for one of each kind.
    """

    electronegativity_difference = (
        mg.periodic_table.elements[element_a]["electronegativity_miedema"]
        - mg.periodic_table.elements[element_b]["electronegativity_miedema"]
    )
    return -P * (electronegativity_difference**2)


def calculate_WS_enthalpy_component(
    element_a: str, element_b: str, Q: Number
) -> Number:
    """Calculates the Wigner-Seitz radius discontinuity contribution to the
    gamma factor in the Miedema model of mixing enthalpy.  See equation 1 of:
    http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations.enthalpy

    Parameters
    ----------

    element_a
        The periodic table symbol of element A
    element_b
        The periodic table symbol of element B
    Q
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

    :group: calculations.enthalpy

    Parameters
    ----------

    element_a
        The periodic table symbol of element A
    element_b
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

    :group: calculations.enthalpy

    Parameters
    ----------

    elements
        The elements being used to calculate the surface concentration.
    volumes
        The atomic volumes of the elements.
    composition
        Dictionary containing the percentage of each element in the surface
        composition.
    """

    reduced_vol_a = composition[elements[0]] * (volumes[0] ** (2.0 / 3.0))
    reduced_vol_b = composition[elements[1]] * (volumes[1] ** (2.0 / 3.0))

    return reduced_vol_a / (reduced_vol_a + reduced_vol_b)


def calculate_corrected_volume(
    element_a: str, element_b: str, surface_concentration_a: Number
):
    """Calculates the corrected volume of element_a in an alloy with element_b,
    as defined by the Meidema model.  See equation 2 of:
    http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations.enthalpy

    Parameters
    ----------

    element_a
        The element for which to correct the volume.
    element_b
        The other element in the alloy.
    surface_concentration_a
        The surface concentration of element_a, as calculated by:
        :func:`~metallurgy.enthalpy.calculate_surface_concentration`.

    """

    pure_volume_a = mg.periodic_table.elements[element_a]["volume_miedema"]

    electronegativity_difference = (
        mg.periodic_table.elements[element_a]["electronegativity_miedema"]
        - mg.periodic_table.elements[element_b]["electronegativity_miedema"]
    )

    valence_factor = None
    if element_a in ["Ca", "Sr", "Ba"]:
        valence_factor = 0.04
    elif element_a in ["Ru", "Rh", "Pd", "Os", "Ir", "Pt", "Au"]:
        valence_factor = 0.07

    if valence_factor is None:
        if mg.periodic_table.elements[element_a]["series"] == "alkaliMetal":
            valence_factor = 0.14
        elif mg.periodic_table.elements[element_a]["valence_electrons"] == 2:
            valence_factor = 0.1
        elif mg.periodic_table.elements[element_a]["valence_electrons"] == 3:
            valence_factor = 0.07
        else:
            valence_factor = 0.04

    f_AB = 1 - surface_concentration_a

    corrected_volume_a = (pure_volume_a ** (2.0 / 3.0)) * (
        1 + valence_factor * f_AB * electronegativity_difference
    )

    return corrected_volume_a


def calculate_interface_enthalpy(
    element_a: str, element_b: str, volume_a: Number
) -> Number:
    """Calculates the interfacial enthalpy term of the Miedema model.  See
    equation 1 of: http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations.enthalpy

    Parameters
    ----------

    element_a
        The periodic table symbol of element A.
    element_b
        The periodic table symbol of element B.
    volume_a
        The atomic volume of element A.

    """

    density_a = mg.periodic_table.elements[element_a][
        "wigner_seitz_electron_density"
    ]
    density_b = mg.periodic_table.elements[element_b][
        "wigner_seitz_electron_density"
    ]

    _gamma = gamma(element_a, element_b)
    if _gamma is not None:
        interface_enthalpy = (
            2
            * volume_a
            * _gamma
            / (density_a ** (-1.0 / 3.0) + density_b ** (-1.0 / 3.0))
        )

        return interface_enthalpy


def mixing_enthalpy(alloy: Union[mg.Alloy, str, dict]):
    """Calculates the Miedema model mixing enthalpy.  See equation 15a of:
    http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations.enthalpy

    Parameters
    ----------

    alloy
        Alloy to calculate the mixing enthalpy of.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_enthalpy(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    if alloy.num_elements > 1:

        element_pairs = [
            (a, b)
            for idx, a in enumerate(alloy.elements)
            for b in alloy.elements[idx + 1 :]
        ]

        total_mixing_enthalpy = 0
        for pair in element_pairs:
            tmp_composition = {}
            sub_composition = 0
            for element in pair:
                sub_composition += alloy.composition[element]
            for element in pair:
                tmp_composition[element] = (
                    alloy.composition[element] / sub_composition
                )

            surface_concentration_a = None
            volume_a = mg.periodic_table.elements[pair[0]]["volume_miedema"]
            volume_b = mg.periodic_table.elements[pair[1]]["volume_miedema"]

            if volume_a is None or volume_b is None:
                return None

            for _ in range(10):

                surface_concentration_a = calculate_surface_concentration(
                    pair, [volume_a, volume_b], tmp_composition
                )

                volume_a = calculate_corrected_volume(
                    pair[0], pair[1], surface_concentration_a
                )

                volume_b = calculate_corrected_volume(
                    pair[1], pair[0], 1 - surface_concentration_a
                )

            interface_ab = calculate_interface_enthalpy(
                pair[0], pair[1], volume_a
            )
            interface_ba = calculate_interface_enthalpy(
                pair[1], pair[0], volume_b
            )

            if interface_ab is not None and interface_ba is not None:

                chemical_enthalpy = (
                    alloy.composition[pair[0]]
                    * alloy.composition[pair[1]]
                    * (
                        (1 - surface_concentration_a) * interface_ab
                        + surface_concentration_a * interface_ba
                    )
                )
                total_mixing_enthalpy += chemical_enthalpy

            else:
                return None

    else:
        total_mixing_enthalpy = 0.0

    return total_mixing_enthalpy


def mixing_Gibbs_free_energy(alloy: Union[mg.Alloy, str, dict]) -> Number:
    """Calculates the Gibbs free energy of mixing.

    :group: calculations.enthalpy

    Parameters
    ----------

    alloy
        Alloy to calculate the Gibbs free energy of mixing of.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_Gibbs_free_energy(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    mix_enthalpy = mixing_enthalpy(alloy)
    melting_temperature = mg.linear_mixture(alloy, "melting_temperature")
    mixing_entropy = mg.entropy.mixing_entropy(alloy)

    if (
        mix_enthalpy is None
        or melting_temperature is None
        or mixing_entropy is None
    ):
        return None

    return (
        (mix_enthalpy * 1e3)
        - melting_temperature * mixing_entropy * mg.constants.idealGasConstant
    )


def calculate_topological_enthalpy(alloy):
    """Calculates the topological enthalpy. See equation 16b of
    http://dx.doi.org/10.1016/j.cpc.2016.08.013

    :group: calculations.enthalpy

    Parameters
    ----------

    alloy
        Alloy to calculate the topological enthalpy of.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mismatch_PHS(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    topological_enthalpy = 0
    for element in alloy.composition:
        topological_enthalpy += (
            mg.periodic_table.elements[element]["fusion_enthalpy"]
            * alloy.composition[element]
        )

    return topological_enthalpy


def mismatch_PHS(alloy: Union[mg.Alloy, str, dict]) -> Number:
    """Calculates the mismatch PHS factor. See
    https://doi.org/10.1016/j.intermet.2012.11.020.

    :group: calculations.enthalpy

    Parameters
    ----------

    alloy
        Alloy to calculate the PHS factor of.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mismatch_PHS(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    mix_enthalpy = mixing_enthalpy(alloy)
    mismatch_entropy = mg.entropy.mismatch_entropy(alloy)

    if mix_enthalpy is not None and mismatch_entropy is not None:
        return mix_enthalpy * mismatch_entropy

    return None


def mixing_PHS(alloy):
    """Calculates the mixing PHS factor. See
    https://doi.org/10.1016/j.intermet.2012.11.020.

    :group: calculations.enthalpy

    Parameters
    ----------

    alloy
        Alloy to calculate the PHS factor of.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_PHS(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    mix_enthalpy = mixing_enthalpy(alloy)
    mixing_entropy = mg.entropy.mixing_entropy(alloy)

    if mix_enthalpy is not None and mixing_entropy is not None:
        return mix_enthalpy * mixing_entropy

    return None


def mixing_PHSS(alloy: Union[mg.Alloy, str, dict]) -> Number:
    """Calculates the mismatch PHS factor. See
    https://doi.org/10.1016/j.intermet.2012.11.020.

    :group: calculations.enthalpy

    Parameters
    ----------

    alloy
        Alloy to calculate the PHSS factor of.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mixing_PHSS(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    mix_enthalpy = mixing_enthalpy(alloy)
    mixing_entropy = mg.entropy.mixing_entropy(alloy)
    mismatch_entropy = mg.entropy.mismatch_entropy(alloy)

    if (
        mix_enthalpy is None
        or mixing_entropy is None
        or mismatch_entropy is None
    ):
        return None

    return mix_enthalpy * mixing_entropy * mismatch_entropy


def thermodynamic_factor(alloy: Union[mg.Alloy, str, dict]) -> Number:
    """Calculates the thermodynamic factor. See equation 11 of
    https://doi.org/10.1016/j.matdes.2020.108835.

    :group: calculations.enthalpy

    Parameters
    ----------

    alloy
        Alloy to calculate the thermodynamic factor of mixing of.

    """

    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [thermodynamic_factor(a) for a in list(alloy)]

    if not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    melting_temperature = mg.linear_mixture(alloy, "melting_temperature")
    mix_enthalpy = mixing_enthalpy(alloy)
    mixing_entropy = mg.entropy.mixing_entropy(alloy)

    if (
        melting_temperature is None
        or mix_enthalpy is None
        or mixing_entropy is None
    ):
        return None

    return (melting_temperature * mixing_entropy) / (
        np.abs(mix_enthalpy * 1e3) + 1e-10
    )
