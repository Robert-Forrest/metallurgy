import metallurgy as mg


def test_alloy_creation():

    alloy_from_string = mg.Alloy("Fe20Ag80")

    alloy_from_dict = mg.Alloy({"Fe": 20, "Ag": 80})

    assert alloy_from_string.__dict__ == alloy_from_dict.__dict__


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
