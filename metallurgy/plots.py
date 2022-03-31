import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll


def binary(alloys, data, xlabel=None, ylabel=None, labels=None, scatter_data=None, use_colorline=False, save_path=None):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    elements = []
    for alloy in alloys:
        for element in alloy.elements:
            if element not in elements:
                elements.append(element)

    percentages = []
    for alloy in alloys:
        if elements[0] in alloy.composition:
            percentages.append(alloy.composition[elements[0]]*100)
        else:
            percentages.append(0)

    if use_colorline:
        lc = colorline(data[0], data[1], ax1, z=percentages)
        cbar = plt.colorbar(lc)
        cbar.set_label(elements[0] + " %", rotation=270)

    elif isinstance(data[0], list):
        for i in range(len(data)):
            label = None
            if labels is not None:
                label = labels[i]

            ax1.plot(percentages, data[i], label=label)
    else:
        ax1.plot(percentages, data)

    if scatter_data is not None:
        for scatter_datum in scatter_data:
            ax1.scatter(scatter_datum['data'][0], scatter_datum['data'][1],
                        marker=scatter_datum['marker'], label=scatter_datum['label'], edgecolors='k', zorder=20)
        ax1.legend(loc="best")
    ax1.autoscale()

    if not isinstance(data[0], list) and not use_colorline:
        ax2 = ax1.twiny()
        ax2.set_xticks(ax1.get_xticks())
        ax2.set_xbound(ax1.get_xbound())
        ax2.set_xticklabels([int(100 - x) for x in ax1.get_xticks()])

        ax1.set_xlabel(elements[0] + " %")
        ax2.set_xlabel(elements[1] + " %")
        ax2.grid(False)

    if xlabel is not None:
        ax1.set_xlabel(xlabel)
    if ylabel is not None:
        ax1.set_ylabel(ylabel)

    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path)
    else:
        plt.show()

    plt.cla()
    plt.clf()
    plt.close()


def colorline(x, y, ax, z=None, cmap='jet', norm=plt.Normalize(0.0, 100.0), linewidth=2, alpha=1.0):
    """
    http://nbviewer.ipython.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
    http://matplotlib.org/examples/pylab_examples/multicolored_line.html
    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width
    """

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    # to check for numerical input -- this is a hack
    if not hasattr(z, "__iter__"):
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)

    lc = mcoll.LineCollection(segments, array=z, cmap=cmap, norm=norm,
                              linewidth=linewidth, alpha=alpha)

    ax.add_collection(lc)
    return lc


def make_segments(x, y):
    """
    Create list of line segments from x and y coordinates, in the correct format
    for LineCollection: an array of the form numlines x (points per line) x 2 (x
    and y) array
    """

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    return segments
