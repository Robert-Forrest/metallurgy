from .alloy import Alloy


def generate_alloys(elements, step=1, minPercent=0, maxPercent=100, quaternary=None):

    compositions = []
    allPercentages = []
    percentages = [minPercent - step, minPercent - step, minPercent - step]
    while percentages[0] <= maxPercent:
        percentages[0] += step
        percentages[1] = minPercent - step
        percentages[2] = minPercent - step
        while percentages[1] <= maxPercent:
            percentages[1] += step
            percentages[2] = minPercent - step
            while percentages[2] <= maxPercent:
                percentages[2] += step
                if(sum(percentages) == 100):
                    allPercentages.append(percentages[:])
                    composition_str = ""
                    for i in range(len(elements)):
                        if(percentages[i] > 0):
                            composition_str += elements[i] + \
                                str(percentages[i])

                    if quaternary is not None:
                        composition_str = "(" + composition_str + ")" + str(
                            100 - quaternary[1]) + quaternary[0] + str(quaternary[1])

                    compositions.append(Alloy(composition_str))

    return compositions, allPercentages
