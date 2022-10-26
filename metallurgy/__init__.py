"""Metallurgy

A tool for manipulating alloy compositions, and calculation of their approximate
characteristics based on the linear mixture of elemental properties.
"""

from elementy import PeriodicTable

from .alloy import Alloy
from .linear_mixture import linear_mixture
from .deviation import deviation
from .calculate import calculate, get_property_function
from . import properties
from . import density
from . import valence
from . import entropy
from . import enthalpy
from . import radii
from . import viscosity
from . import price
from . import generate
from . import ratios
from . import plots
from . import analyse
from . import constants

# from . import rdf

periodic_table = PeriodicTable()
model = None


def set_model(model_in):
    """
    Sets a model to be used by metallurgy to provide predictions of alloy
    properties. Optional.

    Parameters
    ----------
    model_in : Cerebral model
        A model which takes alloy compositions as input, and produces
        material property predicitions as output.
    """
    global model
    model = model_in


def get_model():
    """Returns the model set for use in predicting material properties."""
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
    # "rdf",
    "plots",
    "generate",
    "calculate",
    "properties",
    "analyse",
    "constants",
    "model",
    "set_model",
    "get_model",
    "get_property_function",
]
