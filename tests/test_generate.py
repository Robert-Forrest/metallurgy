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


def test_requirements():

    required_elements = {
        'Cu': {
            'min': 0.2,
            'max': 0.6
        },
        'Fe': {
            'min': 0.0,
            'max': 1.0
        },
        'Ni': {
            'min': 0.01,
            'max': 0.99
        }

    }
    random_alloy = mg.generate.random_alloy(required_elements=required_elements)

    for element in required_elements:
        if required_elements[element]['min'] > 0:
            assert element in random_alloy.composition
