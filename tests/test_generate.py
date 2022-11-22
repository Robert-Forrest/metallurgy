import pytest

import metallurgy as mg


def test_random_alloy(random_alloy=None):
    if random_alloy is None:
        random_alloy = mg.generate.random_alloy()
    assert sum(random_alloy.composition.values()) == pytest.approx(1.0)


def test_random_alloys():

    num_alloys = 100
    random_alloys = mg.generate.random_alloys(num_alloys)

    assert len(random_alloys) == num_alloys

    for random_alloy in random_alloys:
        test_random_alloy(random_alloy)


def test_generate_binary_alloys():

    elements = ["Cu", "Zr"]

    step = 1
    alloys, percentages = mg.generate.binary(elements, step)
    assert len(alloys) == len(percentages) == 101
    assert alloys[0].composition == {elements[0]: 1.0}
    assert alloys[-1].composition == {elements[1]: 1.0}

    step = 2
    alloys, percentages = mg.generate.binary(elements, step)
    assert len(alloys) == len(percentages) == 51
    assert alloys[0].composition == {elements[0]: 1.0}
    assert alloys[-1].composition == {elements[1]: 1.0}

    step = 0.5
    alloys, percentages = mg.generate.binary(elements, step)
    assert len(alloys) == len(percentages) == 201
    assert alloys[0].composition == {elements[0]: 1.0}
    assert alloys[-1].composition == {elements[1]: 1.0}


def test_generate_ternary_alloys():

    elements = ["Cu", "Zr", "Al"]

    step = 1
    alloys, percentages = mg.generate.ternary(elements, step)
    assert len(alloys) == len(percentages) == 5151
    assert alloys[0].composition == {elements[0]: 1.0}
    assert alloys[-1].composition == {elements[2]: 1.0}

    step = 2
    alloys, percentages = mg.generate.ternary(elements, step)
    assert len(alloys) == len(percentages) == 1326
    assert alloys[0].composition == {elements[0]: 1.0}
    assert alloys[-1].composition == {elements[2]: 1.0}


def check_constraints(alloys, constraints):
    for alloy in alloys:
        for element in constraints["percentages"]:
            if constraints["percentages"][element]["min"] > 0:
                assert element in alloy.composition

            if element in alloy.composition:
                assert (
                    alloy.composition[element]
                    >= constraints["percentages"][element]["min"]
                )
                assert (
                    alloy.composition[element]
                    <= constraints["percentages"][element]["max"]
                )

                if "precedence" in constraints["percentages"][element]:
                    for other_element in constraints["percentages"]:
                        if element == other_element:
                            continue

                        if other_element in alloy.composition:
                            if (
                                "precedence"
                                in constraints["percentages"][other_element]
                            ):
                                if (
                                    constraints["percentages"][element][
                                        "precedence"
                                    ]
                                    > constraints["percentages"][
                                        other_element
                                    ]["precedence"]
                                ):
                                    assert (
                                        alloy.composition[element]
                                        >= alloy.composition[other_element]
                                    )

            else:
                assert constraints["percentages"][element]["min"] == 0


def test_constraints():

    num_alloys = 100

    constraint_sets = [
        {
            "percentages": {
                "Cu": {"min": 0.2, "max": 0.6},
                "Fe": {"min": 0.0, "max": 1.0},
                "Ni": {"min": 0.01, "max": 0.99, "precedence": 1},
            },
            "max_elements": 10,
            "min_elements": 1,
            "percentage_step": 0.01,
        },
        {
            "percentages": {
                "Zr": {"min": 0.45, "max": 0.65},
                "Ti": {"min": 0.0, "max": 0.2},
                "Cu": {"min": 0.0, "max": 0.3},
                "Ni": {"min": 0.0, "max": 0.3},
                "Al": {"min": 0.0, "max": 0.2},
            },
            "max_elements": 5,
            "min_elements": 1,
            "percentage_step": 0.005,
        },
    ]

    for constraint in constraint_sets:
        random_alloys = mg.generate.random_alloys(
            num_alloys,
            min_elements=constraint["min_elements"],
            max_elements=constraint["max_elements"],
            percentage_constraints=constraint["percentages"],
            percentage_step=constraint["percentage_step"],
        )

        check_constraints(random_alloys, constraint)


def test_mixture():

    A = mg.Alloy("Cu50Zr50")

    mixed = mg.generate.mixture([A])

    assert mixed.composition == A.composition

    B = mg.Alloy("Fe50Ni50")

    mixed = mg.generate.mixture([A, B])

    assert mixed.composition == {
        "Cu": 0.25,
        "Zr": 0.25,
        "Fe": 0.25,
        "Ni": 0.25,
    }

    mixed = mg.generate.mixture([A, B], [0.9, 0.1])

    assert mixed.composition == {
        "Cu": 0.45,
        "Zr": 0.45,
        "Fe": 0.05,
        "Ni": 0.05,
    }

    C = mg.Alloy(
        "Cu50Zr50",
        constraints={
            "percentages": {"Cu": {"min": 0.1, "max": 0.6}},
            "max_elements": 2,
            "min_elements": 1,
        },
    )

    mixed = mg.generate.mixture([C])

    assert mixed.composition == C.composition

    mixed = mg.generate.mixture([C, B])

    assert len(mixed.elements) <= 2
    assert mixed.composition["Cu"] <= 0.6
    assert mixed.composition["Cu"] >= 0.1
