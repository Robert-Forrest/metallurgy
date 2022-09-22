import metallurgy as mg


def test_melting_temperature():
    assert mg.deviation("Cu", "atomic_number") == 0

    assert (
        mg.deviation({"Cu": 0.5, "Zr": 0.5}, "melting_temperature") == 385.115
    )
