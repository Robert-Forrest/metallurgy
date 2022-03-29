import metallurgy as mg
from .alloy import Alloy


def linear_mixture(alloy, feature_name, periodic_table=None, data=None):

    if not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if periodic_table is None:
        periodic_table = mg.periodic_table

    if data is None:
        data = periodic_table.get_data(feature_name, alloy.elements)

    if not data['symbol'].isin(alloy.elements).all():
        return None

    mixed_property = 0
    for element in alloy.elements:
        mixed_property += alloy.composition[element] * \
            data[data['symbol'] == element][feature_name].iloc[0]

    return mixed_property
