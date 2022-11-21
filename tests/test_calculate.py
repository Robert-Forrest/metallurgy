import metallurgy as mg


def test_calculate_property_name():
    assert mg.calculate(
        {"Cu": 0.5, "Zr": 0.5}, "melting_temperature_linearmix"
    ) == mg.linear_mixture({"Cu": 0.5, "Zr": 0.5}, "melting_temperature")

    assert mg.calculate(
        {"Cu": 0.5, "Zr": 0.5}, "melting_temperature_deviation"
    ) == mg.deviation({"Cu": 0.5, "Zr": 0.5}, "melting_temperature")


def test_calculate_property_name_list():

    multi_calc = mg.calculate(
        {"Cu": 0.5, "Zr": 0.5}, ["melting_temperature", "mass"]
    )

    assert len(multi_calc) == 2
    assert "melting_temperature" in multi_calc and "mass" in multi_calc

    assert mg.calculate(
        {"Cu": 0.5, "Zr": 0.5}, ["melting_temperature_linearmix"]
    )["melting_temperature_linearmix"] == mg.linear_mixture(
        {"Cu": 0.5, "Zr": 0.5}, "melting_temperature"
    )
