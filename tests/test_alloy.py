import metallurgy as mg


def test_alloy_creation():
    alloy_from_string = mg.Alloy("Fe20Ag80")

    alloy_from_dict = mg.Alloy({"Fe": 20, "Ag": 80})

    assert alloy_from_string == alloy_from_dict


def test_alloy_to_string():
    alloy = mg.Alloy({"Fe": 20, "Ag": 80})
    assert alloy.to_string() == "Ag80Fe20"


def test_alloy_element_deletion():
    num_alloys = 100
    random_alloys = mg.generate.random_alloys(
        num_alloys,
        min_elements=2,
        max_elements=2,
    )

    for alloy in random_alloys:
        alloy.remove_element(alloy.elements[0])
        assert alloy.to_string() == alloy.elements[0] + "100"

    random_alloys = mg.generate.random_alloys(
        num_alloys,
        min_elements=2,
        max_elements=2,
    )

    for alloy in random_alloys:
        del alloy.composition[alloy.elements[0]]
        assert alloy.to_string() == alloy.elements[0] + "100"


def test_alloy_equality():
    assert mg.Alloy("Fe20Ag80") == "Fe20Ag80" == mg.Alloy("Ag80Fe20")


def test_sub_alloy_parsing():
    assert (
        mg.Alloy("(Fe20Ag80)50Xe50")
        == mg.Alloy("Xe50(Fe20Ag80)50")
        == "Fe10Ag40Xe50"
    )


def test_multiple_round():
    assert mg.alloy.multiple_round(0.015, 0.02) == 0.02
    assert mg.alloy.multiple_round(0.015, 0.01) == 0.02
    assert mg.alloy.multiple_round(0.12345, 0.03) == 0.12
    assert mg.alloy.multiple_round(0.12345, 0.2) == 0.2


def test_structure():
    assert mg.Alloy("Cu", "A1") == "Cu100[A1]"
    assert mg.Alloy("CuZr", "A1") == "Cu50Zr50[A1]"
    assert mg.Alloy("CuZr", "B2") == "Cu50Zr50[B2]"
    assert mg.Alloy("CuZr", "L1_0") == "Cu50Zr50[L1_0]"
    assert mg.Alloy("ZrCu", "D2_1") == "Cu85.72Zr14.28[D2_1]"
    assert mg.Alloy("CuZr", "D2_1") == "Zr85.72Cu14.28[D2_1]"
    assert (
        mg.Alloy("Fe38As38Cu12Sc12[D0_3]").to_string()
        == "Fe38As38Cu12Sc12[D0_3]"
    )

    assert (
        mg.Alloy(
            {"Fe": 0.6666666666666666, "O": 0.3333333333333333},
            structure="BaPtSb",
        )
        == "Fe66.667O33.333[BaPtSb]"
    )

    assert mg.Alloy("CuZr", "D5_3") == "Cu70Zr30[D5_3]"


def test_structure_change():
    a = mg.Alloy("CuZr", "A1")
    a.structure = "A2"
    assert a == "Cu50Zr50[A2]"

    a = mg.Alloy("CuZr", "B1")
    a.structure = "D0_23"
    assert a == "Cu75Zr25[D0_23]"


def test_structure_element_order():
    assert mg.Alloy("Cu", "A1").elements_structure_order == ["Cu"]
    assert mg.Alloy("CuZr", "B1").elements_structure_order == ["Cu", "Zr"]
    assert mg.Alloy("CuZr", "C32").elements_structure_order == ["Cu", "Zr"]
    assert mg.Alloy("Cu66.67Mn33.33", "C32").elements_structure_order == [
        "Mn",
        "Cu",
    ]
    assert mg.Alloy("CuZr", "D5_3").elements_structure_order == ["Cu", "Zr"]


def test_scale_conversion():
    assert mg.Alloy("Cu50Zr50") == mg.Alloy("Cu0.5Zr0.5")
    assert mg.Alloy("Cu99.9Zr0.1") == mg.Alloy("Cu0.999Zr0.001")
