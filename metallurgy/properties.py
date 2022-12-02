"""Utility functions handling property units and property name formatting."""

# A variety of units for some alloy properties
pretty_names = {
    "Dmax": "$D_{\mathrm{max}}$",
    "Tl": "$T_l$",
    "Tg": "$T_g$",
    "Tx": "$T_x$",
    "deltaT": "$\Delta T$",
}

units = {
    "Dmax": "mm",
    "Tl": "K",
    "Tg": "K",
    "Tx": "K",
    "deltaT": "K",
    "price_linearmix": "\\$/kg",
    "price": "\\$/kg",
    "mixing_enthalpy": "kJ/mol",
    "mixing_Gibbs_free_energy": "kJ/mol",
}
inverse_units = {}
for property_name in units:
    if "/" not in units[property_name]:
        inverse_units[property_name] = "1/" + units[property_name]
    else:
        split_units = units[property_name].split("/")
        inverse_units[property_name] = split_units[1] + "/" + split_units[0]


def pretty_name(property_name: str) -> str:
    """Returns a nicely formatted version of an alloy property name

    Parameters
    ==========

    property_name : str
        Name of the property to format.

    """
    name = ""
    property_name_parts = property_name.split("_")
    if "linearmix" in property_name or "deviation" in property_name:
        if len(property_name_parts) > 1:
            if property_name_parts[-1] == "linearmix":
                name = r"$\Sigma$ "
            elif property_name_parts[-1] == "deviation":
                name = r"$\delta$ "
            name += " ".join(
                word.title() for word in property_name_parts[0:-1]
            )
    elif property_name in pretty_names:
        name += pretty_names[property_name]
    else:
        name += " ".join(word.title() for word in property_name_parts)
    return name
