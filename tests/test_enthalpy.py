import pytest
import metallurgy as mg


def test_mixing_enthalpy():
    assert mg.enthalpy.mixing_enthalpy("Cu") == 0
    assert mg.enthalpy.mixing_enthalpy("Cu50Zr50") == pytest.approx(
        -22.598395865085948
    )


def test_mixing_Gibbs_free_energy():
    assert mg.enthalpy.mixing_Gibbs_free_energy("Cu") == 0
    assert mg.enthalpy.mixing_Gibbs_free_energy("CuZr") == pytest.approx(
        -35625.153905259554
    )


def test_mismatch_PHS():
    assert mg.enthalpy.mismatch_PHS("Fe") == 0
    assert mg.enthalpy.mismatch_PHS("CuZr") == pytest.approx(
        -4.661624378630986
    )


def test_mixing_PHS():
    assert mg.enthalpy.mixing_PHS("Fe") == 0
    assert mg.enthalpy.mixing_PHS("CuZr") == pytest.approx(-20.325638757692836)


def test_mixing_PHSS():
    assert mg.enthalpy.mixing_PHSS("Fe") == 0
    assert mg.enthalpy.mixing_PHSS("CuZr") == pytest.approx(-4.192797298966486)


def test_thermodynamic_factor():
    assert mg.enthalpy.thermodynamic_factor("Fe") == 0
    assert mg.enthalpy.thermodynamic_factor("CuZr") == pytest.approx(
        0.06936776640549777
    )


def test_gamma():
    assert mg.enthalpy.gamma("Cu", "Zr") == pytest.approx(-13.605582368214959)


def test_calculate_QPR():
    assert mg.enthalpy.calculate_QPR("Cu", "Fe") == (132.54, 14.1, 0)
    assert mg.enthalpy.calculate_QPR("Fe", "C") == (115.62, 12.3, 2.1)
    assert mg.enthalpy.calculate_QPR("B", "C") == (99.64, 10.6, 0)


def test_wigner_seitz_discontinuity():
    assert mg.enthalpy.wigner_seitz_electron_density_discontinuity_delta(
        "Cu", "Zr"
    ) == pytest.approx(0.06107640860538699)


def test_topological_enthalpy():
    assert mg.enthalpy.calculate_topological_enthalpy(
        {"Cu": 0.5, "Zr": 0.5}
    ) == pytest.approx(13.629999999999999)
