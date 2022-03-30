import pytest
import metallurgy as mg


def test_mixing_enthalpy():
    assert mg.enthalpy.calculate_mixing_enthalpy("Cu50Zr50") == pytest.approx(-16.988864976589436)
    assert mg.enthalpy.calculate_mixing_enthalpy("Cu") == 0
