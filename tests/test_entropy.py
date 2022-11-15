import pytest
import metallurgy as mg


def test_mixing_entropy():
    assert mg.entropy.mixing_entropy("Cu") == 0
    assert mg.entropy.mixing_entropy("Cu50Zr50") == pytest.approx(
        0.8994283877067366
    )
    assert mg.entropy.mixing_entropy(["Fe", "Cu50Zr50"]) == [
        0,
        pytest.approx(0.8994283877067366),
    ]


def test_mismatch_entropy():
    assert mg.entropy.mismatch_entropy("Fe") == 0
    assert mg.entropy.mismatch_entropy("Cu50Zr50") == pytest.approx(
        0.2062812071467913
    )
    assert mg.entropy.mismatch_entropy(["Fe", "Cu50Zr50"]) == [
        0,
        pytest.approx(0.2062812071467913),
    ]


def test_ideal_entropy():
    assert mg.entropy.ideal_entropy("Xe") == 0
    assert mg.entropy.ideal_entropy("XeAr") == pytest.approx(
        0.6931471805599453
    )
    assert mg.entropy.ideal_entropy("GdFeNi") == pytest.approx(
        1.0986112890009436
    )
    assert mg.entropy.ideal_entropy(["Xe", "XeAr", "GdFeNi"]) == [
        0,
        pytest.approx(0.6931471805599453),
        pytest.approx(1.0986112890009436),
    ]


def test_ideal_entropy_xia():
    assert mg.entropy.ideal_entropy_xia("Xe") == 0
    assert mg.entropy.ideal_entropy_xia("XeAr") == pytest.approx(
        0.7343892084076673
    )
    assert mg.entropy.ideal_entropy_xia("XeArNi") == pytest.approx(
        1.4162078890605776
    )
    assert mg.entropy.ideal_entropy_xia(["Xe", "XeAr", "XeArNi"]) == [
        0,
        pytest.approx(0.7343892084076673),
        pytest.approx(1.4162078890605776),
    ]
