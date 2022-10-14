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


def test_requirements():

    num_alloys = 100

    percentage_constraints = {
        "Cu": {"min": 0.2, "max": 0.6},
        "Fe": {"min": 0.0, "max": 1.0},
        "Ni": {"min": 0.01, "max": 0.99, "precedence": 1},
    }
    random_alloys = mg.generate.random_alloys(
        num_alloys, percentage_constraints=percentage_constraints
    )

    for random_alloy in random_alloys:
        for element in percentage_constraints:
            if percentage_constraints[element]["min"] > 0:
                assert element in random_alloy.composition

            if element in random_alloy.composition:
                assert (
                    random_alloy.composition[element]
                    >= percentage_constraints[element]["min"]
                )
                assert (
                    random_alloy.composition[element]
                    <= percentage_constraints[element]["max"]
                )

                if "precedence" in percentage_constraints[element]:
                    for other_element in percentage_constraints:
                        if element == other_element:
                            continue

                        if other_element in random_alloy.composition:
                            if (
                                "precedence"
                                in percentage_constraints[other_element]
                            ):
                                if (
                                    percentage_constraints[element][
                                        "precedence"
                                    ]
                                    > percentage_constraints[other_element][
                                        "precedence"
                                    ]
                                ):
                                    assert (
                                        random_alloy.composition[element]
                                        >= random_alloy.composition[
                                            other_element
                                        ]
                                    )

            else:
                assert percentage_constraints[element]["min"] == 0


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
