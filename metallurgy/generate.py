import numpy as np
import elementy

from .alloy import Alloy


def random_alloy(
        min_elements=1,
        max_elements=10,
        percentage_constraints={},
        allowed_elements=[e.symbol for e in elementy.PeriodicTable().elements]):

    if isinstance(percentage_constraints, (list)):
        parsed_percentage_constraints = {}
        for element in percentage_constraints:
            parsed_percentage_constraints[element] = {}
        percentage_constraints = parsed_percentage_constraints

    if min_elements < max_elements:
        num_extra_elements = np.random.randint(
            min_elements, max_elements)
    else:
        num_extra_elements = max_elements
    num_extra_elements -= len(percentage_constraints)

    if num_extra_elements > 0:
        other_elements = allowed_elements[:]
        for element in percentage_constraints:
            if element in other_elements:
                other_elements.remove(element)
        elements = list(percentage_constraints.keys()) + \
            list(np.random.choice(other_elements, num_extra_elements, replace=False))

    else:
        elements = list(np.random.choice(
            list(percentage_constraints.keys()),
            num_extra_elements + len(percentage_constraints.keys()),
            replace=False))

    percentages = list(np.random.dirichlet(np.ones(len(elements)), size=1)[0])

    composition = {}
    for j in range(len(elements)):
        composition[elements[j]] = percentages[j]

    alloy = Alloy(
        composition,
        {
            'percentages': percentage_constraints,
            'min_elements': min_elements,
            'max_elements': max_elements
        }
    )
    alloy.rescale()

    if len(alloy.elements) == 0:
        return random_alloy(
            min_elements=min_elements,
            max_elements=max_elements,
            percentage_constraints=percentage_constraints,
            allowed_elements=allowed_elements)

    return alloy


def random_alloys(num_alloys,
                  min_elements=1,
                  max_elements=10,
                  percentage_constraints={},
                  allowed_elements=[e.symbol for e in elementy.PeriodicTable().elements]):

    return [
        random_alloy(
            min_elements,
            max_elements,
            percentage_constraints,
            allowed_elements
        ) for _ in range(num_alloys)]
