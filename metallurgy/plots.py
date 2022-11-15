import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mcoll
import matplotlib as mpl
import ternary as ternary_plt

import metallurgy as mg


def plot(alloys, data, label=None):
    if isinstance(alloys[0], mg.Alloy):
        num_elements = len(mg.analyse.find_unique_elements(alloys))
    elif isinstance(alloys[0], list) and isinstance(alloys[0][0], mg.Alloy):
        num_elements = len(
            mg.analyse.find_unique_elements(
                [alloy for sublist in alloys for alloy in sublist]
            )
        )

    if num_elements == 2:
        return binary(alloys, data, ylabel=label)
    elif num_elements == 3:
        return ternary(alloys, data, label=label)
    elif num_elements == 4:
        return quaternary(alloys, data, label=label)
    else:
        raise NotImplementedError(
            "No plotting available for "
            + str(alloys[0].num_elements)
            + " element alloys."
        )


def binary(
    alloys,
    data,
    xlabel=None,
    ylabel=None,
    labels=None,
    scatter_data=None,
    use_colorline=False,
    save_path=None,
):
    """Plots an alloy property across a binary alloy composition.

    :group: plots

    Parameters
    ----------

    alloys : List[mg.Alloy, str, dict]
        The alloys across the binary composition
    """

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
            percentages.append(alloy.composition[elements[0]] * 100)
        else:
            percentages.append(0)

    percentages, data = zip(*sorted(zip(percentages, data)))

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
            ax1.scatter(
                scatter_datum["data"][0],
                scatter_datum["data"][1],
                marker=scatter_datum["marker"],
                label=scatter_datum["label"],
                edgecolors="k",
                zorder=20,
            )
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


def ternary(
    alloys,
    data,
    step=0.01,
    scatter_data=None,
    save_path=None,
    label=None,
    title=None,
    vmin=None,
    vmax=None,
    ax=None,
    showColorbar=True,
):
    """Plots an alloy property across a ternary alloy composition.

    :group: plots

    Parameters
    ----------

    alloys : List[mg.Alloy, str, dict]
        The alloys across the ternary composition
    """

    scale = 1 / step
    multiple = 0.1 / step
    fontsize = 10
    tick_fontsize = 6
    tick_offset = 0.018
    gridline_width = 0.3
    gridline_style = "--"
    gridline_color = "white"

    elements = []
    for alloy in alloys:
        for element in alloy.elements:
            if element not in elements:
                elements.append(element)

    if not isinstance(data, dict):
        data = list(data)

        heatmap_data = dict()

        for i in range(len(data)):
            percent_A = 0
            percent_B = 0

            if elements[0] in alloys[i].composition:
                percent_A = round(alloys[i].composition[elements[0]] / step, 2)
            if elements[1] in alloys[i].composition:
                percent_B = round(alloys[i].composition[elements[1]] / step, 2)

            heatmap_data[(percent_A, percent_B)] = data[i]

        data = heatmap_data

    if ax is None:
        figure, tax = ternary_plt.figure(scale=scale)
    else:
        figure, tax = ternary_plt.figure(scale=scale, ax=ax)

    tax.get_axes().axis("off")

    tax.gridlines(
        color=gridline_color,
        multiple=multiple,
        linewidth=gridline_width,
        ls=gridline_style,
    )

    tax.set_axis_limits({"b": [0, 100], "l": [0, 100], "r": [0, 100]})
    tax.get_ticks_from_axis_limits(multiple=multiple)
    tax.set_custom_ticks(
        fontsize=tick_fontsize, offset=tick_offset, multiple=multiple
    )

    tax.left_axis_label(elements[2] + " %", fontsize=fontsize, offset=0.12)
    tax.right_axis_label(elements[1] + " %", fontsize=fontsize, offset=0.12)
    tax.bottom_axis_label(elements[0] + " %", fontsize=fontsize, offset=0.12)
    tax.clear_matplotlib_ticks()

    tax.set_title(title, pad=15)

    viridis_cmap = mpl.cm.get_cmap("viridis")
    tax.heatmap(
        heatmap_data,
        cmap=viridis_cmap,
        vmax=vmax,
        vmin=vmin,
        cbarlabel=label,
        colorbar=showColorbar,
    )

    if scatter_data is not None:
        for scatter_datum in scatter_data:
            tax.scatter(
                scatter_datum["data"],
                marker=scatter_datum["marker"],
                label=scatter_datum["label"],
                edgecolors="k",
                zorder=20,
            )

        tax.legend(loc="upper right", handletextpad=0.1, frameon=False)

    tax.get_axes().set_aspect(1)
    tax._redraw_labels()

    if ax is None:
        if save_path is None:
            tax.show()
        else:
            tax.savefig(save_path + ".png")

        tax.close()
        figure.clf()


def quaternary(quaternary_alloys, data, label):

    unique_percentages = mg.analyse.find_unique_percentages(
        quaternary_alloys[-1]
    )

    quaternary_element = list(unique_percentages.keys())[
        np.argmin([len(unique_percentages[e]) for e in unique_percentages])
    ]
    ternary_elements = []
    for element in unique_percentages:
        if element != quaternary_element:
            ternary_elements.append(element)

    vmin = min(y for x in data for y in x)
    vmax = max(y for x in data for y in x)

    columns = int(np.ceil(np.sqrt(len(quaternary_alloys))))
    rows = int(np.ceil(len(quaternary_alloys) / columns))
    numGridCells = columns * rows
    gridExcess = numGridCells - len(quaternary_alloys)

    fig = plt.figure(figsize=(4 * columns, 4 * rows))

    lastAx = None
    for i in reversed(range(len(quaternary_alloys))):
        iRow = i // columns
        iCol = i % columns

        ax = plt.subplot2grid((rows, columns), (iRow, iCol))

        if gridExcess != 0 and iRow == (rows - 1):
            if gridExcess % 2 == 0:
                ax = plt.subplot2grid((rows, columns), (iRow, iCol + 1))
            else:
                ax = plt.subplot2grid(
                    (rows, columns * 2), (iRow, 1 + (iCol * 2)), colspan=2
                )

        if lastAx is None:
            lastAx = ax

        unique_percentages = mg.analyse.find_unique_percentages(
            quaternary_alloys[i]
        )

        if quaternary_element in unique_percentages:
            quaternary_percentage = (
                unique_percentages[quaternary_element][0] * 100
            )
        else:
            quaternary_percentage = 0.0

        remaining_percentage = round(100 - quaternary_percentage, 2)
        remaining_percentage_str = pretty_percentage(str(remaining_percentage))
        quaternary_percentage_str = pretty_percentage(
            str(round(quaternary_percentage, 2))
        )

        title = (
            "("
            + "".join(ternary_elements)
            + ")$_{"
            + remaining_percentage_str
            + "}$"
            + quaternary_element
            + "$_{"
            + quaternary_percentage_str
            + "}$"
        )

        ternary_alloys = quaternary_alloys[i][:]
        for j in range(len(ternary_alloys)):
            ternary_alloys[j].remove_element(quaternary_element)

        ternary(
            ternary_alloys,
            data[i],
            ax=ax,
            vmin=vmin,
            vmax=vmax,
            title=title,
            label=label,
            showColorbar=False,
        )

    viridis_cmap = mpl.cm.get_cmap("viridis")

    cax = fig.add_axes(
        [
            lastAx.get_position().x1 + 0.01,
            lastAx.get_position().y0 + 0.03,
            0.0075,
            lastAx.get_position().height,
        ]
    )

    colorbar = fig.colorbar(
        mpl.cm.ScalarMappable(
            norm=mpl.colors.Normalize(vmin=vmin, vmax=vmax),
            cmap=viridis_cmap,
        ),
        cax=cax,
    )
    colorbar.set_label(label, labelpad=20, rotation=270)

    plt.show()
    plt.clf()
    plt.cla()
    plt.close()


def colorline(
    x,
    y,
    ax,
    z=None,
    cmap="viridis",
    norm=plt.Normalize(0.0, 100.0),
    linewidth=2,
    alpha=1.0,
):
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

    lc = mcoll.LineCollection(
        segments,
        array=z,
        cmap=cmap,
        norm=norm,
        linewidth=linewidth,
        alpha=alpha,
    )

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


def pretty_percentage(string):
    while string[-1] == "0":
        string = string[:-1]
    if string[-1] == ".":
        string = string[:-1]
    return string
