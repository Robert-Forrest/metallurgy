"""Module providing an interface to all other calculation functions provided by
metallurgy.
"""


import inspect
from dataclasses import fields
from numbers import Number
from typing import Callable, Iterable, List, Optional, Union

import elementy
import numpy as np

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
    """Get the function responsible for calculating a particular
    property, if it exists in metallurgy.

    :group: utils

    Parameters
    ----------

    property_name
        Name of the property to get the function for.

    """

    # Get all modules in metallurgy
    modules = inspect.getmembers(mg, inspect.ismodule)
    for module in modules:
        # For each function in the module, check if the name
        # matches the property
        for func in list_functions(module[1]):
            if func == property_name:
                return getattr(module[1], func)


def get_all_elemental_properties(add_suffixes: bool = False) -> List[str]:
    properties = []

    for p in fields(elementy.element.Element):
        if p.name in ["name", "symbol"]:
            continue
        if (
            p.type in [int, float, Optional[float]]
            and p.name not in properties
        ):
            if not add_suffixes:
                properties.append(p.name)
            else:
                properties.append(p.name + "_linearmix")
                properties.append(p.name + "_deviation")
                properties.append(p.name + "_range")
                properties.append(p.name + "_minimum")
                properties.append(p.name + "_maximum")

    return properties


def get_all_complex_properties() -> List[str]:
    properties = []

    # Get all modules in metallurgy
    modules = inspect.getmembers(mg, inspect.ismodule)
    for module in modules:
        for func in list_functions(module[1]):
            argspec = inspect.getfullargspec(getattr(module[1], func))
            if (
                "alloy" in argspec.args
                and len(argspec.args) == 1
                and func not in properties
            ):
                properties.append(func)
    return properties


def get_all_properties(add_suffixes: bool = False) -> List[str]:
    """Returns every calculable property for alloy compositions.

    :group: utils
    """

    properties = (
        get_all_elemental_properties(add_suffixes=add_suffixes)
        + get_all_complex_properties()
    )

    return properties


def get_per_element_values(alloy, property_name):
    per_element_values = []
    for element in alloy.elements:
        # Get the current element's value of the property from elementy
        value = mg.periodic_table.elements[element][property_name]

        # Return None if no data for the element
        if value is None:
            return None
        # Use the first entry for the property if multiple
        elif isinstance(value, list):
            value = value[0]

        # If not numerical data, return None
        if not isinstance(value, Number):
            return None

        per_element_values.append(value)
    return per_element_values


def calculate(
    alloy: Union[mg.Alloy, str, dict],
    property_name: Optional[Union[str, List[str]]] = None,
    uncertainty: bool = False,
) -> Union[float, None, List[Union[float, None]]]:
    """Returns the a particular property calculated for an alloy, using other
    calculation functions provided by metallurgy. The property_name must match
    a function name in a metallurgy module, or be suffixed with _linearmix or
    _deviation to denote linear mixture or deviation of an elemental property.

    :group: calculations

    Parameters
    ----------

    alloy
        The alloy for which to calculate a property.
    property_name
        The property to calculate for the alloy.
    uncertainty
        If using a cerebral model, activate dropout layers during inference and
        gather uncertainty information.
    """
    if property_name is None:
        property_name = [p for p in get_all_properties(add_suffixes=True)]

    if isinstance(property_name, Iterable) and not isinstance(
        property_name, (str, dict)
    ):
        model_properties = []
        analytical_properties = []
        if mg.get_model() is not None:
            import cerebral as cb

            model = mg.get_model()
            for p in property_name:
                if p in [
                    f["name"]
                    for f in cb.models.get_model_prediction_features(model)
                ]:
                    model_properties.append(p)

        for p in property_name:
            if p not in model_properties:
                analytical_properties.append(p)

        values = {}
        for p in analytical_properties:
            values[p] = calculate(alloy, p)

        if len(model_properties) > 0:
            predictions = cb.models.predict(
                model, alloy, uncertainty=uncertainty
            )
            for p in model_properties:
                values[p] = predictions[p]

        return values

    # If we have a predictive model available to use
    if mg.get_model() is not None:
        import cerebral as cb

        # Check if the property is an output of the model, if so use the model
        # and return the prediction
        model = mg.get_model()
        if property_name in [
            f["name"] for f in cb.models.get_model_prediction_features(model)
        ]:
            return cb.models.predict(model, alloy, uncertainty=uncertainty)[
                property_name
            ]

    # Check for simple linear mixture or deviations of elemental properties
    if "_linearmix" in property_name:
        return mg.linear_mixture(alloy, property_name.split("_linearmix")[0])
    elif "_deviation" in property_name:
        return mg.deviation(alloy, property_name.split("_deviation")[0])
    elif "_range" in property_name:
        return mg.range(alloy, property_name.split("_range")[0])
    elif "_maximum" in property_name:
        return mg.maximum(alloy, property_name.split("_maximum")[0])
    elif "_minimum" in property_name:
        return mg.minimum(alloy, property_name.split("_minimum")[0])

    # Otherwise, check all function names to find a match to the property
    property_function = get_property_function(property_name)
    if property_function is not None:
        return property_function(alloy)

    # If all else fails, try a simple linear mixture again
    return mg.linear_mixture(alloy, property_name)


def linear_mixture(
    alloy: Union[mg.Alloy, str, dict], property_name: str
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the linear mixture of a particular elemental property of an
    alloy.

    See equation 5 of the paper "Machine-learning improves understanding of
    glass formation in metallic systems" for definition of the linear mixture:
    https://pubs.rsc.org/en/content/articlelanding/2022/dd/d2dd00026a

    :group: calculations

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the linear mixture.
    property_name : str
        The elemental property to calculate the linear mixture of.

    """

    # If a list of alloys is given, return a list of linear mixture data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [linear_mixture(a, property_name) for a in list(alloy)]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    # Calculate the linear mixture
    mixed_property = 0.0
    for element in alloy.elements:
        # Get the current element's value of the property from elementy
        value = mg.periodic_table.elements[element][property_name]

        # Return None if no data for the element
        if value is None:
            return None
        # Use the first entry for the property if multiple
        elif isinstance(value, list):
            value = value[0]

        # If not numerical data, return None
        if not isinstance(value, Number):
            return None

        # Element's contribution to the linear mixture, weighted by composition
        mixed_property += alloy.composition[element] * value

    return mixed_property


def deviation(
    alloy: Union[mg.Alloy, str, dict], property_name: str
) -> Union[float, None, List[Union[float, None]]]:
    """Returns the deviation of a particular elemental property in an
    alloy.

    See equation 6 of the paper "Machine-learning improves understanding of
    glass formation in metallic systems" for definition of the deviation:
    https://pubs.rsc.org/en/content/articlelanding/2022/dd/d2dd00026a

    :group: calculations

    Parameters
    ----------

    alloy
        The alloy for which to calculate the deviation.
    property_name
        The elemental property to calculate the linear mixture of.

    """

    # If a list of alloys is given, return a list of deviation data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [deviation(a, property_name) for a in list(alloy)]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    # Deviation only makes sense for multi-element alloys
    if len(alloy.elements) > 1:
        # If property is numerical, calculate the deviation of the values
        if isinstance(
            mg.periodic_table.elements[alloy.elements[0]][property_name],
            (Number, list),
        ):
            # Calculate the mean value of the property in the alloy
            mean = 0
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][property_name]

                # Return None if property is None
                if value is None:
                    return None

                # Take first entry if property is a list
                if isinstance(value, list):
                    value = value[0]

                # Return None if property is not numerical
                if not isinstance(value, Number):
                    return None

                mean += alloy.composition[element] * value

            # Calculate the deviation of the property in the alloy
            total_deviation = 0
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][property_name]

                # Return None if property is None
                if value is None:
                    return None

                # Take first entry if property is a list
                if isinstance(value, list):
                    value = value[0]

                # Return None if property is not numerical
                if not isinstance(value, Number):
                    return None

                total_deviation += alloy.composition[element] * (
                    (value - mean) ** 2
                )

            return total_deviation**0.5

        # If property is non-numerical, calculate the shannon entropy of the
        # values
        else:
            # Count unique values of the property
            value_count = {}
            for element in alloy.elements:
                value = mg.periodic_table.elements[element][property_name]
                if value is None:
                    return None

                if value not in value_count:
                    value_count[value] = 0
                value_count[value] += alloy.composition[element]

            # Shannon entropy is only non-zero if multiple unique values
            if len(value_count) > 1:
                shannonEntropy = 0
                for value in value_count:
                    shannonEntropy -= value_count[value] * np.log(
                        value_count[value]
                    )
                return shannonEntropy
            else:
                return 0.0

    # Single element alloys have zero deviation
    else:
        return 0.0


def range(
    alloy: Union[mg.Alloy, str, dict], property_name: str
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the range of a particular elemental property of an
    alloy.

    :group: calculations

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the range.
    property_name : str
        The elemental property to calculate the linear mixture of.

    """

    # If a list of alloys is given, return a list of linear mixture data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [mg.range(a, property_name) for a in list(alloy)]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    per_element_values = get_per_element_values(alloy, property_name)
    if per_element_values is None or None in per_element_values:
        return None
    return float(
        np.abs(np.max(per_element_values) - np.min(per_element_values))
    )


def maximum(
    alloy: Union[mg.Alloy, str, dict], property_name: str
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the maximum of a particular elemental property of an alloy.

    :group: calculations

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the maximum.
    property_name : str
        The elemental property to calculate the linear mixture of.

    """

    # If a list of alloys is given, return a list of linear mixture data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [maximum(a, property_name) for a in list(alloy)]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    raw_values = get_per_element_values(alloy, property_name)
    if raw_values is not None:
        values = []
        for v in raw_values:
            if v is not None:
                values.append(v)

        return float(np.max(values))


def minimum(
    alloy: Union[mg.Alloy, str, dict], property_name: str
) -> Union[Number, None, List[Union[Number, None]]]:
    """Returns the minimum of a particular elemental property of an alloy.

    :group: calculations

    Parameters
    ----------

    alloy : Alloy, str, dict
        The alloy for which to calculate the minimum.
    property_name : str
        The elemental property to calculate the linear mixture of.

    """

    # If a list of alloys is given, return a list of linear mixture data
    if isinstance(alloy, Iterable) and not isinstance(alloy, (str, dict)):
        return [minimum(a, property_name) for a in list(alloy)]

    # Convert input alloy to an Alloy instance if not already
    elif not isinstance(alloy, mg.Alloy):
        alloy = mg.Alloy(alloy)

    raw_values = get_per_element_values(alloy, property_name)
    if raw_values is not None:
        values = []
        for v in raw_values:
            if v is not None:
                values.append(v)
        return float(np.min(values))
