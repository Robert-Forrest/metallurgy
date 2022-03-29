import metallurgy as mg
from .alloy import Alloy


def deviation(alloy, feature_name, periodic_table=None, data=None):

    if not isinstance(alloy, Alloy):
        alloy = Alloy(alloy)

    if periodic_table is None:
        periodic_table = mg.periodic_table

    if data is None:
        data = periodic_table.get_data(feature_name, alloy.elements)

    if not data['symbol'].isin(alloy.elements).all():
        return None

    if(len(alloy.elements) > 1):
        mean = 0
        for element in alloy.elements:
            mean += alloy.composition[element] * \
                data[data['symbol'] == element][feature_name].iloc[0]

        deviation = 0
        for element in alloy.elements:
            deviation += alloy.composition[element] * \
                ((data[data['symbol'] == element][feature_name].iloc[0] -
                  mean)**2)

        return deviation**0.5

    else:
        return 0
