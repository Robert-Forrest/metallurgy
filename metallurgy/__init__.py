from elementy.periodictable import PeriodicTable

from .linear_mixture import linear_mixture
from .deviation import deviation
from .alloy import Alloy
from . import features
from . import density
from . import valence
from . import entropy
from . import enthalpy
from . import radii
from . import viscosity
from . import price
from . import generate
from . import ratios
from .calculate import calculate
from . import plots
from . import analyse

periodic_table = PeriodicTable()
model = None


def set_model(model_in):
    global model
    model = model_in


def get_model():
    return model


__all__ = [
    "periodic_table",
    "Alloy",
    "linear_mixture",
    "deviation",
    "density",
    "valence",
    "entropy",
    "enthalpy",
    "radii",
    "price",
    "viscosity",
    "ratios",
    "plots",
    "generate",
    "calculate",
    "features",
    "analyse",
    'model',
    'set_model',
    'get_model'
]
