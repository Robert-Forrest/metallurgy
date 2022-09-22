import metallurgy as mg


def test_melting_temperature():
    assert (
        mg.linear_mixture({"Cu": 0.5, "Zr": 0.5}, "melting_temperature")
        == 1742.885
    )

    assert mg.linear_mixture(
        [{"Cu": 0.5, "Zr": 0.5}, {"Cu": 0.25, "Zr": 0.75}],
        "melting_temperature",
    ) == [1742.885, 1935.4425]
