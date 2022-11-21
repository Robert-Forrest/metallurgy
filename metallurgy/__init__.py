"""Metallurgy

A tool for manipulating alloy compositions, and calculation of their approximate
characteristics based on the linear mixture of elemental properties.
"""

from typing import Union, Optional, List

import pandas as pd
from elementy import PeriodicTable

from .alloy import Alloy
from .linear_mixture import linear_mixture
from .deviation import deviation
from .calculate import calculate, get_property_function, get_all_properties
from .plots import plot
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


def to_dataframe(
    alloys: Union[list, pd.DataFrame],
    data: Optional[dict] = None,
    properties: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Convert a list of alloys to a Pandas DataFrame

    :group: alloy.utils

    Parameters
    ----------
    alloys
        List of alloys to create a DataFrame
    data
        Dictionary with keys being property names and values being lists of
        property values
    properties
        List of properties to calculate for the alloys.

    """

    if data is not None and properties is not None:
        raise ValueError("Cannot set both data and properties arguments.")

    if not isinstance(alloys, pd.DataFrame):
        alloys_dataframe = pd.DataFrame.from_records(
            [alloy.to_dict() for alloy in alloys]
        )
    else:
        alloys_dataframe = alloys.copy()

    if data is not None:
        alloys_dataframe = pd.concat(
            [alloys_dataframe, pd.DataFrame.from_dict(data)],
            axis=1,
        )
    elif properties is not None:
        property_values = {}
        for p in properties:
            property_values[p] = calculate(alloys, p)

        alloys_dataframe = pd.concat(
            [alloys_dataframe, pd.DataFrame.from_dict(property_values)],
            axis=1,
        )

    return alloys_dataframe


def write_csv(
    alloys: Union[list, pd.DataFrame],
    data: Optional[dict] = None,
    properties: Optional[List[str]] = None,
    filename: str = "alloys",
):
    """Creates a CSV file of alloy data.

    :group: alloy.utils

    Parameters
    ----------
    alloys
        Dataset of alloys to create a CSV file.
    data
        Dictionary with keys being property names and values being lists of
        property values
    properties
        List of properties to calculate for the alloys.
    filename
        Name of the CSV file (will be suffixed with .csv).

    """

    if data is not None and properties is not None:
        raise ValueError("Cannot set both data and properties arguments.")

    if data is not None:
        to_dataframe(alloys, data=data).to_csv(filename + ".csv", index=False)

    elif properties is not None:
        to_dataframe(alloys, properties=properties).to_csv(
            filename + ".csv", index=False
        )


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
    "plot",
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
    "get_all_properties",
    "write_csv",
]
