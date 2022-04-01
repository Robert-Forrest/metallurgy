import metallurgy as mg


def calculate(alloys, feature_name):
    if "_linearmix" in feature_name:
        return mg.linear_mixture(alloys, feature_name.split("_linearmix")[0])
    elif "_deviation" in feature_name:
        return mg.deviation(alloys, feature_name.split("_deviation")[0])
