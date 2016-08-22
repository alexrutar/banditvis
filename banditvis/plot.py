import os

import matplotlib.pyplot as plt
import numpy as np

from .data import VarData
from .simulation import ReMapSim
from .formatting import cmap_colors, mpl_defaults
from .commands import safe_save


def VarPlot(core_dict):
    """
    Makes a Variable plot out of existing data.

    The data is loaded from the data folder, whose location is specified in the
    input dictionary. The loop iterates over files in that folder, and for each
    one adds a plot to the figure.

    Uses plt.savefig to save the plot when finished.

    TODO:
    * add proper label support from user input
    """

    # defaults
    fig, ax = mpl_defaults.plot()

    # add plots
    for i, sub_dict in enumerate(core_dict['sim']):
        y_list = np.loadtxt(
            "{}/data{}.txt".format(core_dict['DataFolder'], i),
            float)
        x_list = core_dict['arg_list']

        cmap = cmap_colors.sequential1[i]

        plt.plot(x_list, y_list,".--",
            linewidth=1,
            color = cmap(0.8),
            label = sub_dict['label'])

    # labels / text
    legend = plt.legend(loc='best', framealpha = 1.0)
    legend.get_frame().set_linewidth(1)
    plt.xlabel(core_dict['xlabel'])
    plt.ylabel(core_dict['ylabel'])
    plt.title(core_dict['PlotTitle'], style='italic')

    # save plot
    plt.savefig(safe_save(core_dict['PlotSave']))

    return None


def HistPlot(core_dict):
    """
    Makes a Histogram plot out of existing data.

    The data is loaded from the data folder, whose location is specified in the
    input dictionary. The loop iterates over files in that folder, and for each
    one adds a plot to the figure.

    Uses plt.savefig to save the plot when finished.

    TODO:
    * move HistData out of this function
    * add support for custom user (x,y)labels, if so desired
    """

    # defaults
    fig, ax = mpl_defaults.plot()

    # variables
    bins = np.linspace(0, np.amax(core_dict['bins']), num = 90)

    # add plots
    for i, sub_dict in enumerate(core_dict['sim']):
        data = np.loadtxt(
            "{}/data{}.txt".format(core_dict['DataFolder'], i),
            float)

        cmap = cmap_colors.sequential1[i]

        avgline = np.average(data)
        plt.axvline(x = avgline, color = cmap(0.5),ls="--" ,linewidth = 1.7)

        plt.hist(data, bins,
            normed=1,
            alpha=0.6,
            facecolor = cmap(0.8),
            label = sub_dict['label'])

    # labels / text
    legend = plt.legend(loc='best', framealpha = 1.0)
    legend.get_frame().set_linewidth(1)
    plt.xlabel('Regret')
    plt.ylabel('Frequency')
    plt.title(core_dict['PlotTitle'], style='italic')

    # save plot
    plt.savefig(safe_save(core_dict['PlotSave']))

    return None