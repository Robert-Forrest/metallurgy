import metallurgy as mg


def test_generate_ternary_alloys():

    elements = ["Cu", "Zr", "Al"]

    step = 1
    alloys, percentages = mg.ternary.generate_alloys(elements, step)
    assert len(alloys) == len(percentages) == 5151

    step = 2
    alloys, percentages = mg.ternary.generate_alloys(elements, step)
    assert len(alloys) == len(percentages) == 1326
