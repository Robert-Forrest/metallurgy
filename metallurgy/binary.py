from .alloy import Alloy


def generate_alloys(elements, step=0.5):

    x = 100
    alloys = []
    percentages = []
    while x >= 0:
        alloys.append(Alloy(
            elements[0] + str(x) + elements[1] + str(100 - x), rescale=False))
        percentages.append(x)
        x -= step

    return alloys, percentages
