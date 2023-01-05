import metallurgy as mg


def test_melting_temperature():

    assert mg.range({"Cu": 0.5, "Zr": 0.5}, "melting_temperature") == 385.115
