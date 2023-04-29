"""Metallurgy

A tool for manipulating alloy compositions, and calculation of their
approximate characteristics based on the linear mixture of elemental
properties.
"""
# isort: skip_file

from typing import List, Optional, Union

import pandas as pd
from elementy import PeriodicTable

from .alloy import Alloy
from . import (
    analyse,
    constants,
    density,
    enthalpy,
    entropy,
    generate,
    plots,
    price,
    properties,
    prototypes,
    radii,
    ratios,
    valence,
    viscosity,
)
from .calculate import (
    calculate,
    deviation,
    get_all_properties,
    get_property_function,
    linear_mixture,
    maximum,
    minimum,
    range,
)
from .plots import plot
from .prototype import Prototype

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
    "Prototype",
    "prototypes",
    "linear_mixture",
    "deviation",
    "range",
    "maximum",
    "minimum",
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
