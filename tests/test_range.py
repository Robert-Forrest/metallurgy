import metallurgy as mg


def test_melting_temperature_range():
    assert mg.range("CuZr", "melting_temperature") == 770.23
