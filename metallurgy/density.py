import metallurgy as mg
from .alloy import Alloy


def calculate_theoretical_density(alloy):
    if isinstance(alloy, list):
        return [calculate_theoretical_density(a) for a in alloy]
    elif not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    data = mg.periodic_table.data

    massFractions = {}
    masses = {}
    totalMass = 0
    for element in alloy.elements:
        masses[element] = data[element]['mass']
        totalMass += masses[element] * alloy.composition[element]

    for element in alloy.elements:
        massFractions[element] = alloy.composition[element] * \
            masses[element] / totalMass

    total = 0
    for element in alloy.elements:
        total += massFractions[element] / \
            data[element]['density']

    return 1 / total
