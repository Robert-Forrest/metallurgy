"""Module providing an interface to all other calculation functions provided by
metallurgy.
"""


import inspect
from typing import Union, List, Callable

import metallurgy as mg


def is_mod_function(mod, func):
    """checks that func is a function defined in module mod"""
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
    """list of functions defined in module mod"""
    return [
        func.__name__
        for func in mod.__dict__.values()
        if is_mod_function(mod, func)
    ]


def get_property_function(property_name: str) -> Union[Callable, None]:
    """Get the function responsible for calculating a particular property, if it
    exists in metallurgy.

    :group: utils

    Parameters
    ----------

    property_name
        Name of the property to get the function for.

    """

    # Get all modules in metallurgy
    modules = inspect.getmembers(mg, inspect.ismodule)
    for module in modules:
        # For each function in the module, check if the name matches the property
        for func in list_functions(module[1]):
            if func == property_name:
                return getattr(module[1], func)


def calculate(
    alloy: Union[mg.Alloy, str, dict], property_name: str
) -> Union[float, None, List[Union[float, None]]]:
    """Returns the a particular property calculated for an alloy, using other
    calculation functions provided by metallurgy. The property_name must match a
    function name in a metallurgy module, or be suffixed with _linearmix or
    _deviation to denote linear mixture or deviation of an elemental property.

    :group: calculations

    Parameters
    ----------

    alloy
        The alloy for which to calculate a property.
    property_name
        The property to calculate for the alloy.
    """

    # If we have a predictive model available to use
    if mg.get_model() is not None:
        import cerebral as cb

        # Check if the property is an output of the model, if so use the model
        # and return the prediction
        model = mg.get_model()
        if property_name in [
            f["name"] for f in cb.models.get_model_prediction_features(model)
        ]:
            return cb.models.predict(model, alloy)[property_name]

    # Check for simple linear mixture or deviations of elemental properties
    if "_linearmix" in property_name:
        return mg.linear_mixture(alloy, property_name.split("_linearmix")[0])
    elif "_deviation" in property_name:
        return mg.deviation(alloy, property_name.split("_deviation")[0])
    # Otherwise, check all function names to find a match to the property
    else:
        property_function = get_property_function(property_name)
        if property_function is not None:
            return property_function(alloy)

        # If all else fails, try a simple linear mixture again
        return mg.linear_mixture(alloy, property_name)
