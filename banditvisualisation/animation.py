import copy

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches

from .simulation import ReMapSim


def HistAnimation(core_dict):
    """
    Makes an animation of a Histogram.

    TODO
    * fix bins
    * custom user labels
    * add support for custom fps
    """

    # defaults
    plt.style.use('bmh')
    mpl.rcParams['toolbar'] = 'None'
    plt.rcParams['font.size'] = 12
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.titlesize'] = 14
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 13
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['legend.edgecolor'] = '#e6e6e6'
    plt.rcParams['legend.facecolor'] = '#ffffff'

    # plot variables
    cmap1 = plt.cm.get_cmap('BuGn')
    cmap2 = plt.cm.get_cmap('Blues')
    fig = plt.figure(figsize=(14,9), facecolor='white')
    ax = fig.add_subplot(1,1,1)
    bins = np.linspace(0,core_dict['bins'][0],100)

    # formatting
    plt.tick_params(
        axis='y',
        which='both',
        left='off',
        right='off')
    plt.tick_params(
        axis='x',
        which='both',
        top='off')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')

    # load data
    data = np.loadtxt(core_dict['data_folder'] + "/data0.txt", float)

    # update function used by the animation
    def _update(num, data):
        nonlocal cmap1, bins, ax

        # clear axes, load data to refresh
        plt.cla()
        data = np.loadtxt(core_dict['data_folder'] + "/data0.txt", float)

        # plots
        plt.axvline(x = np.average(data),
            color = cmap1(0.5),
            ls="--" ,
            linewidth=1.7)
        plt.hist(data, bins,
            alpha=0.6,
            normed=1,
            facecolor=cmap1(0.8),
            label="X ~ Beta(2,5)")

        # labels
        legend = plt.legend(loc='upper right', framealpha = 1.0)
        legend.get_frame().set_linewidth(1)
        plt.title(core_dict['PlotTitle'], style='italic')

        plt.xlabel('Regret')
        plt.ylabel('Frequency')
        ax.set_ylim([0,0.2])
    # build the animation and run it
    my_ani = animation.FuncAnimation(fig, _update,
        fargs=(data, ),
        interval=50)
    plt.show()





def ConfAnimation(core_dict):
    """
    Animates the confidence intervals.

    Since only one cycle is run at a given time, the bandit algorithm is run at
    the same time as the animation rather than using an external data source.

    TODO
    * y limits might not be correct in some cases; specify
    """

    # defaults
    mpl.rcParams['toolbar'] = 'None'
    plt.style.use('bmh')
    plt.rcParams['font.size'] = 12
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.titlesize'] = 12
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['legend.edgecolor'] = '#e6e6e6'
    plt.rcParams['legend.facecolor'] = '#ffffff'

    # map the core_dict to actual objects
    ReMapSim(core_dict['sim'][0])

    # plot variables
    sim = core_dict['sim'][0]['Simulation']
    arms = sim.bandit.n_arms
    title = "Upper Confidence Animation"
    not_picked_color = plt.cm.get_cmap('BuGn')(0.6)
    picked_color = plt.cm.get_cmap('OrRd')(0.6)
    x_labels = ["Mean: "+str(item) for item in sim.bandit.mean_list]
    bar_width = 0.45

    # simulation variables
    horizon = core_dict['horizon']
    confidence = sim.bandit.U_conf
    index = np.arange(arms)

    # initialize the bandit
    for i in range(arms):
        sim.bandit.pullArm(i)

    fig = plt.figure(figsize=(14,9), facecolor='white')
    ax = fig.add_subplot(1,1,1)

    # formatting
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')

    # the animation update function
    def _update(num, confidence):
        nonlocal ax

        # ste bandit 1 timestep
        sim.runStep(1, horizon)
        confidence = sim.bandit.U_conf
        max_confidence = np.amax(sim.bandit.U_conf)

        # clear plot to redraw
        plt.cla()

        # make a bar plot
        bar_list = plt.bar(index, confidence, bar_width,
            align='center',
            color=not_picked_color,
            edgecolor='#e6e6e6')

        # add a maximum line
        plt.axhline(y=max_confidence,
            ls='dashdot',
            xmin=0.0,
            xmax=1.0,
            linewidth=2.0,
            color='#434343')

        # change the colour of the best arm (the picked arm)
        bar_list[np.argmax(confidence)].set_facecolor(picked_color)

        # add dashed lines for the actual mean of each arm
        for i in range(sim.bandit.n_arms):
            x = [i - bar_width/2, i + bar_width/2]
            y = [sim.bandit.mean_list[i], sim.bandit.mean_list[i]]
            plt.plot(x,y,'--',
                linewidth = 2,
                color='#000000',
                ls='dashed',
                mfc='white')

        # add x labels
        plt.xticks(index, x_labels, weight='bold')

        # add two legends:
        #   * a real legend
        #   * one to display interesting information
        picked_color_path = mpatches.Patch(
            color=picked_color,
            label='Arm chosen')
        not_picked_color_path = mpatches.Patch(
            color=not_picked_color,
            label='Arm(s) not chosen')
        legend_1 = plt.legend(
            handles=[picked_color_path, not_picked_color_path],
            loc='upper right')
        plt.gca().add_artist(legend_1)  # prevent legend_2 from overwriting
        legend_1.get_frame().set_linewidth(1)

        blank_path_1 = mpatches.Patch(
            label='Regret: {:04.2f}'.format(sim.bandit.giveRegret()))
        blank_path_2 = mpatches.Patch(
            label='Timestep: {:2d}'.format(sim.bandit.timestep[0]))
        legend_2 = plt.legend(
            handles=[blank_path_1, blank_path_2],
            loc='upper left',
            handlelength=0,
            handletextpad=0)
        legend_2.get_frame().set_linewidth(1)

        # formatting
        ax.grid(False)  # resets grid default
        ax.set_ylim([0,1.2])
        ax.yaxis.grid(True)  # turns horizontal grid on

        plt.title(title)

    # the animation declaration
    my_ani = animation.FuncAnimation(fig, _update,
        fargs=(sim.bandit.U_conf, ),
        interval = 50)  # fargs is used as the data required in update_hist

    plt.show()




def EllipseAnimation(core_dict):
    """
    Animates the confidence intervals.

    Since only one cycle is run at a given time, the bandit algorithm is run at
    the same time as the animation rather than using an external data source.

    TODO
    * y limits might not be correct in some cases; specify
    """

    # defaults
    mpl.rcParams['toolbar'] = 'None'
    plt.style.use('bmh')
    plt.rcParams['font.size'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.titlesize'] = 12
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['legend.edgecolor'] = '#e6e6e6'
    plt.rcParams['legend.facecolor'] = '#ffffff'
    plt.rcParams['legend.numpoints'] = 1

    # map the core_dict sim to actual objects
    ReMapSim(core_dict['sim'][0])

    # simulation variables
    sim = core_dict['sim'][0]['Simulation']
    sim_dict = core_dict['sim'][0]
    arms = sim.bandit.arm_vecs
    mean = np.array(sim.bandit.mean)
    horizon = core_dict['horizon']
    title = "2D Confidence Ellipse Animation"
    # the locations of the perpindicular projection of the arm vector onto the
    # mean vector
    projs = np.array(
        [mean / np.linalg.norm(mean)**2 * np.inner(arm, mean) for arm in arms])
    cmap1 = plt.cm.get_cmap('BuGn')
    cmap2 = plt.cm.get_cmap('Reds')

    # establish plot boundaries
    all_points = np.vstack((arms, mean))
    x_max = np.amax(all_points[:,0])
    x_min = np.amin(all_points[:,0])
    y_max = np.amax(all_points[:,1])
    y_min = np.amin(all_points[:,1])
    x_margin = (x_max-x_min)
    y_margin = (y_max-y_min)
    x_max += x_margin/3
    x_min -= x_margin/5  # less margin on right
    y_max += y_margin/3
    y_min -= y_margin/5  # less margin at bottom

    # set up the figure and axes
    fig = plt.figure(figsize=(14,9), facecolor='white')
    ax = fig.add_subplot(111, axisbg='white')
    ax.set_aspect('equal')

    # initialize the bandit
    for i in range(sim.bandit.n_arms):
        sim.bandit.pullArm(i)


    def plot_ellipse(rho, cov, pos, ax=None, **kwargs):
        """
        Plots an ellipse based on the specified covariance on the parameter rho
        matrix (`cov`). Additional keyword arguments are passed on to the
        ellipse patch artist.

        Parameters
        ----------
            rho : the radius of the ellipse
            cov : The 2x2 covariance matrix to base the ellipse on
            pos : The location of the center of the ellipse. Expects a 2-element
                sequence of [x0, y0].
            ax : The axis that the ellipse will be plotted on. Defaults to the
                current axis.
            Additional keyword arguments are pass on to the ellipse patch.

        Returns
        -------
            A matplotlib ellipse artist
        """
        def eigsorted(cov):
            vals, vecs = np.linalg.eigh(cov)
            order = vals.argsort()[::-1]
            return vals[order], vecs[:,order]

        if ax is None:
            ax = plt.gca()

        vals, vecs = eigsorted(cov)
        theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))

        # width and height are full width, not radius
        width, height = 2 * np.sqrt(rho * vals)
        ellip = mpatches.Ellipse(
            xy=pos,
            width=width,
            height=height,
            angle=theta,
            **kwargs)
        ax.add_artist(ellip)
        return ellip

    # the animation update function
    def _update(num, confidence):
        nonlocal ax

        # step the bandit
        sim.runStep(1, horizon)
        rho = sim.bandit.dim * np.log(sim.bandit.timestep[0])
        G_inv = np.linalg.inv(sim.bandit.G)
        bandit_mean = sim.bandit.U
        chosen_arm = sim.bandit.arm_vecs[np.argmax(sim.bandit.U_conf)]

        # clear plot to redraw
        plt.cla()

        # general formatting
        ax.grid(True)
        ax.set_ylim([y_min,y_max])
        ax.set_xlim([x_min,x_max])
        ax.set_aspect('equal')
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_bbox(dict(
                facecolor='white',
                edgecolor='None',
                alpha=0.65 ))

        # format the axes
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data',0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data',0))

        # remove label option
        if sim_dict['NoAxesTick']:
            ax.set_xticks([])
            ax.set_yticks([])

        # adds circle for normalized bandit
        if sim_dict['Normalized']:
            ax.add_artist(mpatches.Circle(
                xy=(0.,0.),
                radius=1,
                edgecolor='black',
                alpha=0.2,
                facecolor='none'))

        # position of mean vector
        plt.plot([mean[0]],[mean[1]], "o",
            color='black',
            label='True Mean')

        # plot the ellipse and the mean
        plot_ellipse(rho, G_inv, bandit_mean,
            alpha=0.2,
            facecolor=cmap1(0.5),
            edgecolor=cmap1(1.0))
        plt.plot([sim.bandit.U[0]], [sim.bandit.U[1]], "o",
            markerfacecolor=cmap2(0.5),
            markeredgecolor=cmap2(1.0),
            label='Approximated Mean')

        # HelpLines: dashed projection lines to show reward value
        if sim_dict['HelpLines']:
            for proj, arm in zip(projs, arms):
                plt.plot([proj[0], arm[0]], [proj[1], arm[1]],
                    color='black',
                    linestyle='dashdot',
                    linewidth=0.8)
            plt.plot([-mean[0]*50,mean[0]*50],[-mean[1]*50,mean[1]*50], "--",
                linewidth=0.5,
                markersize=3,
                color='black')

        # arm vector points
        plt.plot([arm[0] for arm in sim.bandit.arm_vecs],
            [arm[1] for arm in sim.bandit.arm_vecs], "o",
            markersize=5,
            markerfacecolor=cmap1(0.5),
            markeredgecolor=cmap1(1.0),
            label='Arm Vectors')

        # chosen arm; draws a red circle around it
        plt.plot(chosen_arm[0],chosen_arm[1], "or",
            markersize=10,
            markerfacecolor='none',
            markeredgecolor='red',
            markeredgewidth=2,
            label='Chosen Arm')

        # legend and title
        legend = plt.legend(loc='upper right')
        plt.gca().add_artist(legend)
        legend.get_frame().set_linewidth(1)

        # additional information legend
        blank_path_1 = mpatches.Patch(
            label='Regret: {:04.2f}'.format(sim.bandit.giveRegret()))
        blank_path_2 = mpatches.Patch(
            label='Timestep: {:2d}'.format(sim.bandit.timestep[0]))
        legend_2 = plt.legend(
            handles=[blank_path_1, blank_path_2],
            loc='upper left',
            handlelength=0,
            handletextpad=0)
        legend_2.get_frame().set_linewidth(1)

        plt.title(title)

    # the animation declaration
    my_ani = animation.FuncAnimation(fig, _update,
        fargs=(sim.bandit.U_conf, ),
        interval = 50)  # fargs is used as the data required in update_hist

    plt.show()