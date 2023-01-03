from .prototype import Prototype


def get_prototype(name: str):
    if name in prototypes:
        return prototypes[name]
    else:
        raise NotImplementedError(
            name + " prototype structure has not been implemented"
        )


prototypes = {
    "B2": Prototype(
        name="B2",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
        ],
    ),
    "F5_1": Prototype(
        name="F5_1",
        lattice=[
            [
                0.5,
                -0.28868,
                0.33333,
            ],
            [
                0,
                0.57735,
                0.33333,
            ],
            [
                -0.5,
                -0.28868,
                0.33333,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 2,
                "vector": [
                    "x",
                    "x",
                    "x",
                ],
            },
            {
                "element": 2,
                "vector": [
                    "-x",
                    "-x",
                    "-x",
                ],
            },
        ],
    ),
    "A3'": Prototype(
        name="A3'",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333333,
                    0.66666667,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.6666666667,
                    0.3333333333,
                    0.75,
                ],
            },
        ],
    ),
    "A10": Prototype(
        name="A10",
        lattice=[
            [
                0.5,
                -0.288675,
                0.333333,
            ],
            [
                0,
                0.5773503,
                0.3333333,
            ],
            [
                -0.5,
                -0.288675,
                0.333333,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
        ],
    ),
    "A11": Prototype(
        name="A11",
        lattice=[
            [
                0.5,
                -0.5,
                0,
            ],
            [
                0.5,
                0.5,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "-u",
                    "u",
                    "v",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "u",
                    "-u",
                    "-v",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-(0.5+u)",
                    "0.5+u",
                    "(0.5-v)",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-(0.5-u)",
                    "0.5-u",
                    "0.5+v",
                ],
            },
        ],
    ),
    "A15": Prototype(
        name="A15",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.75,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.25,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.75,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0.75,
                ],
            },
        ],
    ),
    "Ah": Prototype(
        name="Ah",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
        ],
    ),
    "Af": Prototype(
        name="Af",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
        ],
    ),
    "A1": Prototype(
        name="A1",
        lattice=[
            [
                0.5,
                0.5,
                0,
            ],
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
        ],
    ),
    "A2": Prototype(
        name="A2",
        lattice=[
            [
                0.5,
                0.5,
                -0.5,
            ],
            [
                -0.5,
                0.5,
                0.5,
            ],
            [
                0.5,
                -0.5,
                0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
        ],
    ),
    "A4": Prototype(
        name="A4",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    -0.125,
                    -0.125,
                    -0.125,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.125,
                    0.125,
                    0.125,
                ],
            },
        ],
    ),
    "A5": Prototype(
        name="A5",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0.5,
                0.5,
                0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    -0.125,
                    -0.375,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.125,
                    0.375,
                    -0.25,
                ],
            },
        ],
    ),
    "A6": Prototype(
        name="A6",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0.5,
                0.5,
                0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
        ],
    ),
    "A8": Prototype(
        name="A8",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "x",
                    0,
                    0.33333,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    "x",
                    0.66667,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x",
                    "-x",
                    0,
                ],
            },
        ],
    ),
    "A20": Prototype(
        name="A20",
        lattice=[
            [
                0.5,
                -0.5,
                0,
            ],
            [
                0.5,
                0.5,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "-y",
                    "y",
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "y",
                    "-y",
                    -0.25,
                ],
            },
        ],
    ),
    "Lonsdaleite": Prototype(
        name="Lonsdaleite",
        lattice=[
            [
                0.5,
                -0.866025,
                0,
            ],
            [
                0.5,
                0.866025,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.333333,
                    0.666667,
                    1,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.666667,
                    0.333333,
                    "0.5 + z",
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.333333,
                    0.666667,
                    "0.5 - z",
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.666667,
                    0.333333,
                    "-z",
                ],
            },
        ],
    ),
    "A3": Prototype(
        name="A3",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.33333333,
                    0.66666667,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.6666666667,
                    0.3333333333,
                    0.75,
                ],
            },
        ],
    ),
    "A9": Prototype(
        name="A9",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.75,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333,
                    0.66667,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66667,
                    0.33333,
                    0.75,
                ],
            },
        ],
    ),
    "A14": Prototype(
        name="A14",
        lattice=[
            [
                0.5,
                -0.5,
                0,
            ],
            [
                0.5,
                0.5,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "u",
                    "u",
                    "v",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "u",
                    "-u",
                    "-v",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-(0.5+u)",
                    "(0.5+u)",
                    "(0.5-v)",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-(0.5-u)",
                    "(0.5-u)",
                    "(0.5+v)",
                ],
            },
        ],
    ),
    "A17": Prototype(
        name="A17",
        lattice=[
            [
                0.5,
                -0.5,
                0,
            ],
            [
                0.5,
                0.5,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "-u",
                    "u",
                    "v",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "u",
                    "u",
                    "v",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-(0.5+u)",
                    "(0.5+u)",
                    "(0.5-v)",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-(0.5-u)",
                    "(0.5-u)",
                    "(0.5+v)",
                ],
            },
        ],
    ),
    "B1": Prototype(
        name="B1",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
        ],
    ),
    "B4": Prototype(
        name="B4",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.33333,
                    0.66667,
                    "z1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66667,
                    0.33333,
                    "0.5 + z1",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    "z2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    "0.5 + z2",
                ],
            },
        ],
    ),
    "B9": Prototype(
        name="B9",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "x1",
                    0,
                    0.66667,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    "x1",
                    0.33333,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x1",
                    "-x1",
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x2",
                    0,
                    0.166667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    "x2",
                    0.833333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x2",
                    "-x2",
                    0.5,
                ],
            },
        ],
    ),
    "Bh": Prototype(
        name="Bh",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.666667,
                    0.333333,
                    0.5,
                ],
            },
        ],
    ),
    "Bk": Prototype(
        name="Bk",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.333333,
                    0.666667,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.666667,
                    0.333333,
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.666667,
                    0.333333,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.333333,
                    0.666667,
                    0.75,
                ],
            },
        ],
    ),
    "B10": Prototype(
        name="B10",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.75,
                    0.25,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.25,
                    0.75,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    0.25,
                    "z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.75,
                    0.75,
                    "-z",
                ],
            },
        ],
    ),
    "B11": Prototype(
        name="B11",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    -0.25,
                    0.25,
                    "-x1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.25,
                    -0.25,
                    "-x1",
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.25,
                    0.25,
                    "x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    -0.25,
                    "-x2",
                ],
            },
        ],
    ),
    "B12": Prototype(
        name="B12",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    "z1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    "(0.5+z1)",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    "z2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    "(0.5+z2)",
                ],
            },
        ],
    ),
    "B17": Prototype(
        name="B17",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0.5,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0,
                    0.75,
                ],
            },
        ],
    ),
    "B33": Prototype(
        name="B33",
        lattice=[
            [
                0.5,
                -0.5,
                0,
            ],
            [
                0.5,
                0.5,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "-x1",
                    "x1",
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "x1",
                    "-x1",
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x2",
                    "x2",
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x2",
                    "-x2",
                    0.75,
                ],
            },
        ],
    ),
    "B3": Prototype(
        name="B3",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    0.25,
                    0.25,
                ],
            },
        ],
    ),
    "B19": Prototype(
        name="B19",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.25,
                    0,
                    "x1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    -0.25,
                    0,
                    "-x1",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    0.5,
                    "x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.25,
                    -0.25,
                    "-x2",
                ],
            },
        ],
    ),
    "B35": Prototype(
        name="B35",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333,
                    0.66667,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66667,
                    0.33333,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
        ],
    ),
    "Bi": Prototype(
        name="Bi",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66667,
                    0.33333,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333,
                    0.66667,
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    "z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    "0.5-z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    "-z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    "0.5+z",
                ],
            },
        ],
    ),
    "B8_1": Prototype(
        name="B8_1",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    0.75,
                ],
            },
        ],
    ),
    "B8_2": Prototype(
        name="B8_2",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    0.75,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66667,
                    0.33333,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333,
                    0.66667,
                    0.75,
                ],
            },
        ],
    ),
    "B24": Prototype(
        name="B24",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    -0.5,
                ],
            },
        ],
    ),
    "B32": Prototype(
        name="B32",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.125,
                    0.125,
                    0.125,
                ],
            },
            {
                "element": 0,
                "vector": [
                    -0.125,
                    -0.125,
                    -0.125,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.375,
                    0.375,
                    0.375,
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.375,
                    -0.375,
                    -0.375,
                ],
            },
        ],
    ),
    "C1_depleted": Prototype(
        name="C1_depleted",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    0.25,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.25,
                    -0.25,
                    -0.25,
                ],
            },
        ],
    ),
    "C1": Prototype(
        name="C1",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    0.25,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.25,
                    -0.25,
                    -0.25,
                ],
            },
        ],
    ),
    "C3": Prototype(
        name="C3",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    0.25,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.75,
                    0.75,
                    0.75,
                ],
            },
        ],
    ),
    "C9": Prototype(
        name="C9",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.125,
                    0.125,
                    0.125,
                ],
            },
            {
                "element": 0,
                "vector": [
                    -0.125,
                    -0.125,
                    -0.125,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0,
                    0.5,
                ],
            },
        ],
    ),
    "C32": Prototype(
        name="C32",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    0.5,
                ],
            },
        ],
    ),
    "C6": Prototype(
        name="C6",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    "0.5+z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    "0.5-z",
                ],
            },
        ],
    ),
    "C7": Prototype(
        name="C7",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.333333333,
                    0.666666666,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.666666666,
                    0.333333333,
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.333333333,
                    0.666666666,
                    "z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.666666666,
                    0.333333333,
                    "0.5 + z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.333333333,
                    0.666666666,
                    "0.5 - z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.666666666,
                    0.333333333,
                    "-z",
                ],
            },
        ],
    ),
    "C33": Prototype(
        name="C33",
        lattice=[
            [
                0.5,
                -0.28868,
                0.33333,
            ],
            [
                0,
                0.57735,
                0.33333,
            ],
            [
                -0.5,
                -0.28868,
                0.33333,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "z1",
                    "z1",
                    "z1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-z1",
                    "-z1",
                    "-z1",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "z2",
                    "z2",
                    "z2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-z2",
                    "-z2",
                    "-z2",
                ],
            },
        ],
    ),
    "C11_b": Prototype(
        name="C11_b",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0.5,
                0.5,
                0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "z",
                    "z",
                    "1-2*z",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-z",
                    "-z",
                    "-(1-2*z)",
                ],
            },
        ],
    ),
    "C1_b": Prototype(
        name="C1_b",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0.25,
                    0.25,
                    0.25,
                ],
            },
        ],
    ),
    "C19": Prototype(
        name="C19",
        lattice=[
            [
                0.5,
                -0.28868,
                0.33333,
            ],
            [
                0,
                0.57735,
                0.33333,
            ],
            [
                -0.5,
                -0.28868,
                0.33333,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "z",
                    "z",
                    "z",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-z",
                    "-z",
                    "-z",
                ],
            },
        ],
    ),
    "C15": Prototype(
        name="C15",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.125,
                    0.125,
                    0.125,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.875,
                    0.875,
                    0.875,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
        ],
    ),
    "D5_3": Prototype(
        name="D5_3",
        lattice=[
            [
                -0.5,
                0.5,
                0.5,
            ],
            [
                0.5,
                -0.5,
                0.5,
            ],
            [
                0.5,
                0.5,
                -0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0.5,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    "0.25+x2",
                    "x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.75,
                    "0.25-x2",
                    "0.5-x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x2",
                    0.25,
                    "0.25+x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "0.5-x2",
                    0.75,
                    "0.25-x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "0.25+x2",
                    "x2",
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "0.25-x2",
                    "0.5-x2",
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.75,
                    "0.75-x2",
                    " -x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    " 0.75+x2",
                    " 0.5+x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    " -x2",
                    0.75,
                    " 0.75-x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    " 0.5+x2",
                    0.25,
                    " 0.75+x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    " 0.75-x2",
                    " -x2",
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    " 0.75+x2",
                    " 0.5+x2",
                    0.25,
                ],
            },
            {
                "element": 2,
                "vector": [
                    " y3 + z3",
                    " x3 + z3",
                    " x3 + y3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 - y3 + z3",
                    " -x3 + z3",
                    " 0.5 - x3 - y3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " y3 - z3",
                    " 0.5 - x3 - z3",
                    " 0.5 - x3 + y3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 - y3 - z3",
                    " 0.5 + x3 - z3",
                    " x3 - y3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " x3 + y3",
                    " y3 + z3",
                    " z3 + x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 - x3 + y3",
                    " y3 - z3",
                    " 0.5 - z3 - x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " x3 - y3",
                    " 0.5 - y3 - z3",
                    " 0.5 - z3 + x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 - x3 - y3",
                    " 0.5 - y3 + z3",
                    " z3 - x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " z3 + x3",
                    " x3 + y3",
                    " y3 + z3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 - z3 + x3",
                    " x3 - y3",
                    " 0.5 - y3 - z3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " -z3 - x3",
                    " 0.5 - x3 - y3",
                    " 0.5 - y3 + z3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 - z3 - x3",
                    " 0.5 - x3 + y3",
                    " y3 - z3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " -y3 - z3",
                    " -x3 - z3",
                    " -x3 - y3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 + y3 - z3",
                    " x3 - z3",
                    " 0.5 + x3 + y3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " -y3 + z3",
                    " 0.5 + x3 + z3",
                    " 0.5 + x3 - y3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 + y3 + z3",
                    " 0.5 - x3 + z3",
                    " -x3 + y3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " -y3 - x3",
                    " -y3 - z3",
                    " -z3 - x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 - y3 + x3",
                    " -y3 + z3",
                    " 0.5 + z3 + x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " y3 - x3",
                    " 0.5 + y3 + z3",
                    " 0.5 + z3 - x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 + y3 + x3",
                    " 0.5 + y3 - z3",
                    " -z3 + x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " -x3 - z3",
                    " -x3 - y3",
                    " -y3 - z3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 - x3 + z3",
                    " -x3 + y3",
                    " 0.5 + y3 + z3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " x3 - z3",
                    " 0.5 + x3 + y3",
                    " 0.5 + y3 - z3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    " 0.5 + x3 + z3",
                    " 0.5 + x3 - y3",
                    " -y3 + z3",
                ],
            },
        ],
    ),
    "D0_3": Prototype(
        name="D0_3",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.25,
                    -0.25,
                    -0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    0.25,
                    0.25,
                ],
            },
        ],
    ),
    "D5_1": Prototype(
        name="D5_1",
        lattice=[
            [
                0.5,
                -0.2886752,
                0.33333333,
            ],
            [
                0,
                0.57735,
                0.33333333,
            ],
            [
                -0.5,
                -0.2886752,
                0.33333333,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "x",
                    "x",
                    "x",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "0.5-x",
                    "0.5-x",
                    "0.5-x",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x",
                    "-x",
                    "-x",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "0.5+x",
                    "0.5+x",
                    "0.5+x",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "y",
                    "0.5-y",
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    "y",
                    "0.5-y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "0.5-y",
                    0.25,
                    "y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-y",
                    "0.5+y",
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.75,
                    "-y",
                    "0.5+y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "0.5+y",
                    0.75,
                    "-y",
                ],
            },
        ],
    ),
    "D0_19": Prototype(
        name="D0_19",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    0.75,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "x",
                    "2.0*x",
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-2*x",
                    "-x",
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "x",
                    "-x",
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x",
                    "-2*x",
                    0.75,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "2*x",
                    "x",
                    0.75,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x",
                    "x",
                    0.75,
                ],
            },
        ],
    ),
    "D0_9": Prototype(
        name="D0_9",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0,
                    0.5,
                ],
            },
        ],
    ),
    "D0_22": Prototype(
        name="D0_22",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0.5,
                0.5,
                0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    -0.25,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.25,
                    0.25,
                    0.5,
                ],
            },
        ],
    ),
    "D2_d": Prototype(
        name="D2_d",
        lattice=[
            [
                0.5,
                -0.86602540378,
                0,
            ],
            [
                0.5,
                0.86602540378,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
        ],
    ),
    "D5_2": Prototype(
        name="D5_2",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333,
                    0.66667,
                    "z2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66667,
                    0.33333,
                    "-z2",
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333,
                    0.66667,
                    "z3",
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66667,
                    0.33333,
                    "-z3",
                ],
            },
        ],
    ),
    "D7_2": Prototype(
        name="D7_2",
        lattice=[
            [
                -0.5,
                0.5,
                0.5,
            ],
            [
                0.5,
                -0.5,
                0.5,
            ],
            [
                0.5,
                0.5,
                -0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.875,
                    0.125,
                    0.75,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.125,
                    0.875,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "y+z",
                    "z",
                    "y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "0.5-y+z",
                    "z",
                    "0.5-y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "z",
                    "0.5-y+z",
                    "-y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "z",
                    "y+z",
                    "0.5+y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "0.5+y-z",
                    "-z",
                    "0.5+y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-y-z",
                    "-z",
                    "-y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-z",
                    "0.5+y-z",
                    "y",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-z",
                    "-y-z",
                    "0.5-y",
                ],
            },
        ],
    ),
    "E2_1": Prototype(
        name="E2_1",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
        ],
    ),
    "L1_2": Prototype(
        name="L1_2",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
        ],
    ),
    "L6_0": Prototype(
        name="L6_0",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
        ],
    ),
    "L1_3": Prototype(
        name="L1_3",
        lattice=[
            [
                0.5,
                -0.5,
                0,
            ],
            [
                0.5,
                0.5,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
        ],
    ),
    "L2_1": Prototype(
        name="L2_1",
        lattice=[
            [
                0,
                0.5,
                0.5,
            ],
            [
                0.5,
                0,
                0.5,
            ],
            [
                0.5,
                0.5,
                0,
            ],
        ],
        basis=[
            {
                "element": 1,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.25,
                    0.25,
                    0.25,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.75,
                    0.75,
                    0.75,
                ],
            },
        ],
    ),
    "L'2": Prototype(
        name="L'2",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0.5,
                0.5,
                0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.25,
                    -0.25,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    -0.25,
                    0.25,
                    0.5,
                ],
            },
        ],
    ),
    "L1_0": Prototype(
        name="L1_0",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
        ],
    ),
    "ZrGa2": Prototype(
        name="ZrGa2",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                -0.86602540378,
                0.5,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.666667,
                    0.333333,
                    1,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.333333,
                    0.666667,
                    1,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.85,
                    0.15,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.15,
                    0.85,
                    0.5,
                ],
            },
        ],
    ),
    "SiO2-b": Prototype(
        name="SiO2-b",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.52271,
                    0.52271,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.47729,
                    0,
                    0.66666667,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0.47729,
                    0.33333333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.584963,
                    0.83926,
                    0.870667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.16074,
                    0.745703,
                    0.53733367,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.254297,
                    0.415037,
                    0.20400033,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.83926,
                    0.584963,
                    0.129333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.745703,
                    0.16074,
                    0.46266633,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.415037,
                    0.254297,
                    0.79599967,
                ],
            },
        ],
    ),
    "Al2O3-a": Prototype(
        name="Al2O3-a",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.147904,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333333,
                    0.66666667,
                    0.01876267,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333333,
                    0.66666667,
                    0.31457067,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66666667,
                    0.33333333,
                    0.18542933,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66666667,
                    0.33333333,
                    0.48123733,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.352096,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.647904,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333333,
                    0.66666667,
                    0.51876267,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.33333333,
                    0.66666667,
                    0.81457067,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66666667,
                    0.33333333,
                    0.68542933,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.66666667,
                    0.33333333,
                    0.98123733,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.852096,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.306146,
                    0,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66666667,
                    0.02718733,
                    0.08333333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.306146,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.693854,
                    0.693854,
                    0.25,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.97281267,
                    0.63947933,
                    0.08333333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.36052067,
                    0.33333333,
                    0.08333333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.97281267,
                    0.33333333,
                    0.58333333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333333,
                    0.36052067,
                    0.41666667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.66666667,
                    0.63947933,
                    0.58333333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.36052067,
                    0.02718733,
                    0.58333333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.63947933,
                    0.97281267,
                    0.41666667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.02718733,
                    0.66666667,
                    0.41666667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.63947933,
                    0.66666667,
                    0.91666667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0.693854,
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.33333333,
                    0.97281267,
                    0.91666667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.02718733,
                    0.36052067,
                    0.91666667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.306146,
                    0.306146,
                    0.75,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.693854,
                    0,
                    0.75,
                ],
            },
        ],
    ),
    "SiO2-a": Prototype(
        name="SiO2-a",
        lattice=[
            [
                0.5,
                -0.8660254038,
                0,
            ],
            [
                0.5,
                0.8660254038,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.52271,
                    0.52271,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.47729,
                    0,
                    0.66666667,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0.47729,
                    0.33333333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.584963,
                    0.83926,
                    0.870667,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.16074,
                    0.745703,
                    0.53733367,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.254297,
                    0.415037,
                    0.20400033,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.83926,
                    0.584963,
                    0.129333,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.745703,
                    0.16074,
                    0.46266633,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.415037,
                    0.254297,
                    0.79599967,
                ],
            },
        ],
    ),
    "Fe5CoN2": Prototype(
        name="Fe5CoN2",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.18331,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0.49958,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0.34649,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0.67654,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0.99567,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    0,
                    0.83344,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0.5,
                    0,
                    0.17748,
                ],
            },
        ],
    ),
    "Nd2Fe14B": Prototype(
        name="Nd2Fe14B",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0.5,
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
        ],
    ),
    "A7": Prototype(
        name="A7",
        lattice=[
            [
                0.5,
                -0.288675,
                0.333333,
            ],
            [
                0,
                0.5773503,
                0.3333333,
            ],
            [
                -0.5,
                -0.288675,
                0.333333,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "x",
                    "x",
                    "x",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x",
                    "-x",
                    "-x",
                ],
            },
        ],
    ),
    "Alpha B": Prototype(
        name="Alpha B",
        lattice=[
            [
                0.5,
                -0.288675,
                0.333333,
            ],
            [
                0,
                0.57735,
                0.33333,
            ],
            [
                -0.5,
                -0.288675,
                0.33333,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "x1",
                    "x1",
                    "z1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "z1",
                    "x1",
                    "x1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "x1",
                    "z1",
                    "x1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x1",
                    "-x1",
                    "-z1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-z1",
                    "-x1",
                    "-x1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x1",
                    "-z1",
                    "-x1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "x2",
                    "x2",
                    "z2",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "z2",
                    "x2",
                    "x2",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "x2",
                    "z2",
                    "x2",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x2",
                    "-x2",
                    "-z2",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-z2",
                    "-x2",
                    "-x2",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x2",
                    "-z2",
                    "-x2",
                ],
            },
        ],
    ),
    "D2_1": Prototype(
        name="D2_1",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x",
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x",
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    "x",
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    "-x",
                    0.5,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    "x",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    "-x",
                ],
            },
        ],
    ),
    "D0_23": Prototype(
        name="D0_23",
        lattice=[
            [
                -0.5,
                0.5,
                0.5,
            ],
            [
                0.5,
                -0.5,
                0.5,
            ],
            [
                0.5,
                0.5,
                -0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0.5,
                    0,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.75,
                    0.25,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    0.25,
                    0.75,
                    0.5,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "x",
                    "x",
                    0,
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x",
                    "-x",
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "z",
                    "z",
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-z",
                    "-z",
                    0,
                ],
            },
        ],
    ),
    "TiPt_8": Prototype(
        name="TiPt_8",
        lattice=[
            [
                -0.5,
                0.5,
                0.5,
            ],
            [
                0.5,
                -0.5,
                0.5,
            ],
            [
                0.5,
                0.5,
                -0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x1",
                    "x1",
                    "2*x1",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x1",
                    "-x1",
                    "-2*x1",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x1",
                    "-x1",
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x1",
                    "x1",
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    "x2",
                    "x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    0,
                    "-x2",
                    "-x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x2",
                    0,
                    "x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x2",
                    0,
                    "-x2",
                ],
            },
        ],
    ),
    "GaPtNi_2": Prototype(
        name="GaPtNi_2",
        lattice=[
            [
                1,
                0,
                0,
            ],
            [
                0,
                1,
                0,
            ],
            [
                0,
                0,
                1,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    0,
                    0,
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    0.5,
                    0.5,
                    0.5,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0,
                    0.5,
                    0,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0.5,
                    0,
                    0,
                ],
            },
        ],
    ),
    "C12": Prototype(
        name="C12",
        lattice=[
            [
                0.5,
                -0.28868,
                0.33333,
            ],
            [
                0.57735,
                0,
                0.333333,
            ],
            [
                -0.5,
                -0.28868,
                0.33333,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "x1",
                    "x1",
                    "x1",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x1",
                    "-x1",
                    "-x1",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x2",
                    "x2",
                    "x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x2",
                    "-x2",
                    "-x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x3",
                    "x3",
                    "x3",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x3",
                    "-x3",
                    "-x3",
                ],
            },
        ],
    ),
    "CsFeS_2": Prototype(
        name="CsFeS_2",
        lattice=[
            [
                -0.5,
                0.5,
                0.5,
            ],
            [
                0.5,
                -0.5,
                0.5,
            ],
            [
                0.5,
                0.5,
                -0.5,
            ],
        ],
        basis=[
            {
                "element": 0,
                "vector": [
                    "x2",
                    0,
                    "x2",
                ],
            },
            {
                "element": 0,
                "vector": [
                    "-x2",
                    0,
                    "-x2",
                ],
            },
            {
                "element": 1,
                "vector": [
                    "x4",
                    "x4",
                    0,
                ],
            },
            {
                "element": 1,
                "vector": [
                    "-x4",
                    "-x4",
                    0,
                ],
            },
            {
                "element": 2,
                "vector": [
                    0,
                    "x1",
                    "x1",
                ],
            },
            {
                "element": 2,
                "vector": [
                    0,
                    "-x1",
                    "-x1",
                ],
            },
            {
                "element": 2,
                "vector": [
                    "0.5 + x3",
                    0.5,
                    "x3",
                ],
            },
            {
                "element": 2,
                "vector": [
                    "0.5 - x3",
                    0.5,
                    "-x3",
                ],
            },
        ],
    ),
}
