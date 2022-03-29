import metallurgy.parse as parse


class Alloy():
    def __init__(self, compositionSeed):

        if isinstance(compositionSeed, str):
            self.composition = parse.parse_composition_string(compositionSeed)
        elif isinstance(compositionSeed, dict):
            self.composition = parse.parse_composition_dict(compositionSeed)

        self.compositionStr = parse.alloy_to_string(self)

        self.elements = list(self.composition.keys())
