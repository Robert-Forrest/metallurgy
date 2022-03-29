import metallurgy as mg


def test_alloy_creation():

    alloy_from_string = mg.Alloy("Fe20Ag80")

    alloy_from_dict = mg.Alloy({"Fe": 20, "Ag": 80})

    assert alloy_from_string.__dict__ == alloy_from_dict.__dict__
