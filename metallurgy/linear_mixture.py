import elementy
from .alloy import Alloy


def linear_mixture(alloy, featureName=None, data=None):

    if(isinstance(alloy, str)):
        alloy = Alloy(alloy)

    if data is None:
        data = elementy.get_data(featureName, alloy.elements)

    if not data['symbol'].isin(alloy.elements).all():
        return None

    mixed_property = 0
    for element in alloy.elements:
        mixed_property += alloy.composition[element] * \
            data[data['symbol'] == element][featureName].iloc[0]

    return mixed_property
