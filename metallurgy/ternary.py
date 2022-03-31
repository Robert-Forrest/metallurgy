from .alloy import Alloy


def generate_alloys(elements, step=1, minPercent=0, maxPercent=100, quaternary=None):

    compositions = []
    percentages = []

    tmp_percentages = [maxPercent+step]*3
    while tmp_percentages[0] >= minPercent+step:
        tmp_percentages[0] -= step
        tmp_percentages[1] = maxPercent+step
        tmp_percentages[2] = maxPercent+step

        while tmp_percentages[1] >= minPercent+step:
            tmp_percentages[1] -= step
            tmp_percentages[2] = maxPercent + step

            while tmp_percentages[2] >= minPercent+step:
                tmp_percentages[2] -= step

                if(sum(tmp_percentages) == 100):

                    composition_str = ""
                    for i in range(len(elements)):
                        if(tmp_percentages[i] > 0):
                            composition_str += elements[i] + \
                                str(tmp_percentages[i])

                    if quaternary is not None:
                        composition_str = "(" + composition_str + ")" + str(
                            100 - quaternary[1]) + quaternary[0] + str(quaternary[1])

                    alloy = Alloy(composition_str)
                    compositions.append(alloy)
                    percentages.append(list(alloy.composition.values()))

    return compositions, percentages
