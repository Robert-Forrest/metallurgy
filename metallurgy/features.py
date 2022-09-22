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
for feature in units:
    if "/" not in units[feature]:
        inverse_units[feature] = "1/" + units[feature]
    else:
        split_units = units[feature].split("/")
        inverse_units[feature] = split_units[1] + "/" + split_units[0]


def pretty_name(feature_name):

    name = ""
    feature_parts = feature_name.split("_")
    if "linearmix" in feature_name or "deviation" in feature_name:
        if len(feature_parts) > 1:
            if feature_parts[-1] == "linearmix":
                name = r"$\Sigma$ "
            elif feature_parts[-1] == "deviation":
                name = r"$\delta$ "
            name += " ".join(word.title() for word in feature_parts[0:-1])
    else:
        name += " ".join(word.title() for word in feature_parts)
    return name
