import metallurgy.parse as parse


class Alloy():
    def __init__(self, composition):

        self.composition = parse.parse_composition(composition)

        self.compositionStr = parse.alloy_to_string(self)

        self.elements = list(self.composition.keys())
