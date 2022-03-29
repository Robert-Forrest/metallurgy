import metallurgy as mg


def test_melting_temperature():
    assert mg.linear_mixture({"Cu": 0.5, "Zr": 0.5},
                             "melting_temperature") == 1742.885
