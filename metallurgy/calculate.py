import inspect

import metallurgy as mg


def is_mod_function(mod, func):
    ' checks that func is a function defined in module mod '
    return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
    ' list of functions defined in module mod '
    return [func.__name__ for func in mod.__dict__.values()
            if is_mod_function(mod, func)]


def calculate(alloys, feature_name):
    if mg.get_model() is not None:
        import cerebral as cb

        model = mg.get_model()
        if feature_name in [f['name'] for f in cb.models.get_model_prediction_features(model)]:
            return cb.models.predict(model, alloys)[feature_name]

    if "_linearmix" in feature_name:
        return mg.linear_mixture(alloys, feature_name.split("_linearmix")[0])
    elif "_deviation" in feature_name:
        return mg.deviation(alloys, feature_name.split("_deviation")[0])
    else:
        modules = inspect.getmembers(mg, inspect.ismodule)
        for module in modules:
            for func in list_functions(module[1]):
                if func == feature_name:
                    return getattr(module[1], func)(alloys)
