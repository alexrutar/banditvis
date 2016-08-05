import os

import matplotlib.pyplot as plt
import numpy as np

from .data import VarData
from .simulation import ReMapSim
from .formatting import cmap_colors


def _safe_plot_save(file_name):
    """Save a plot safely."""
    if file_name.split("/")[-1][:4] == 'temp':
        plt.savefig(file_name)
    elif not os.path.isfile(file_name):
        plt.savefig(file_name)
    else:
        for i in range(100000):
            if os.path.isfile(file_name.split(".")[0]
                + "{}.".format(i)
                + file_name.split(".")[1]):
                pass
            else:
                plt.savefig(file_name.split(".")[0]
                    + "{}.".format(i)
                    + file_name.split(".")[1])
                break
    return None


def VarPlot(core_dict):
    """
    Makes a Variable plot out of existing data.

    The data is loaded from the data folder, whose location is specified in the
    input dictionary. The loop iterates over files in that folder, and for each
    one adds a plot to the figure.

    Uses _safe_plot_save to save the plot when finished.

    TODO:
    * add proper label support from user input
    * move VarData out of this location
    """

    # defaults
    plt.style.use('bmh')
    plt.rcParams['font.size'] = 10
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 12
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['lines.linewidth'] = 1
    plt.rcParams['axes.titlesize'] = 'medium'
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['legend.edgecolor'] = '#e6e6e6'
    plt.rcParams['legend.facecolor'] = '#ffffff'

    # formatting
    axes = plt.gca()
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['left'].set_color('none')

    # add plots
    for i, sub_dict in enumerate(core_dict['sim']):
        y_list = np.loadtxt(
            "{}/data{}.txt".format(core_dict['data_folder'], i),
            float)
        x_list = core_dict['arg_list']

        cmap = plt.cm.get_cmap(cmap_colors.sequential1[i])

        plt.plot(x_list, y_list,".--",
            linewidth=1,
            color = cmap(0.8),
            label = sub_dict['label'])

    # labels / text
    legend = plt.legend(loc='best', framealpha = 1.0)
    legend.get_frame().set_linewidth(1)
    plt.xlabel('Delta')
    plt.ylabel('Regret')
    plt.title(core_dict['PlotTitle'], style='italic')

    # save plot
    _safe_plot_save(core_dict['PlotSavein'])

    return None



def HistPlot(core_dict):
    """
    Makes a Histogram plot out of existing data.

    The data is loaded from the data folder, whose location is specified in the
    input dictionary. The loop iterates over files in that folder, and for each
    one adds a plot to the figure.

    Uses _safe_plot_save to save the plot when finished.

    TODO:
    * move HistData out of this function
    * add support for custom user (x,y)labels, if so desired
    """

    # defaults
    plt.style.use('bmh')
    plt.rcParams['font.size'] = 10
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 12
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titlesize'] = 'medium'
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['legend.edgecolor'] = '#e6e6e6'
    plt.rcParams['legend.facecolor'] = '#ffffff'

    # formatting
    axes = plt.gca()
    axes.spines['right'].set_color('none')
    axes.spines['top'].set_color('none')
    axes.spines['left'].set_color('none')

    # variables
    bins = np.linspace(0, np.amax(core_dict['bins']), num = 90)

    # add plots
    for i, sub_dict in enumerate(core_dict['sim']):
        data = np.loadtxt(
            "{}/data{}.txt".format(core_dict['data_folder'], i),
            float)

        cmap = plt.cm.get_cmap(cmap_colors.sequential1[i])

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
    _safe_plot_save(core_dict['PlotSave'])

    return None