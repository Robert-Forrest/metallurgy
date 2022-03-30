import metallurgy as mg


def test_generate_binary_alloys():

    elements = ["Cu", "Zr"]

    step = 1
    alloys, percentages = mg.binary.generate_alloys(elements, step)
    assert len(alloys) == len(percentages) == 101

    step = 2
    alloys, percentages = mg.binary.generate_alloys(elements, step)
    assert len(alloys) == len(percentages) == 51

    step = 0.5
    alloys, percentages = mg.binary.generate_alloys(elements, step)
    assert len(alloys) == len(percentages) == 201
