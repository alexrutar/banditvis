import matplotlib as mpl
import matplotlib.pyplot as plt

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

class cmap_colors:
    sequential1 = [plt.cm.get_cmap(name) for name in ['Blues', 'Greens', 'Reds', 'BuGn',
        'BuPu','GnBu', 'Greys', 'Oranges',
        'OrRd','PuBu', 'PuBuGn', 'PuRd',
        'Purples', 'RdPu', 'YlGn', 'YlGnBu']]
    sequential2 = [plt.cm.get_cmap(name) for name in ['afmhot', 'autumn', 'bone', 'cool',
        'copper', 'gist_heat', 'gray', 'hot',
        'pink', 'spring', 'summer', 'winter']]

class mpl_defaults:
    def ani():
        """
        Default style used for all animations
        """
        plt.style.use('bmh')
        mpl.rcParams['toolbar'] = 'None'
        plt.rcParams['font.size'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 12
        plt.rcParams['figure.titlesize'] = 12
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['axes.labelweight'] = 'bold'
        plt.rcParams['legend.edgecolor'] = '#e6e6e6'
        plt.rcParams['legend.facecolor'] = '#ffffff'
        plt.rcParams['legend.numpoints'] = 1

        fig = plt.figure(figsize=(14,9), facecolor='white')
        ax = fig.add_subplot(111, axisbg='white')

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)

        return (fig, ax)
    def plot():
        """
        Default style used for all plots
        """
        plt.style.use('bmh')
        plt.rcParams['font.size'] = 10
        plt.rcParams['xtick.labelsize'] = 8
        plt.rcParams['ytick.labelsize'] = 8
        plt.rcParams['legend.fontsize'] = 10
        plt.rcParams['figure.titlesize'] = 12
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.labelsize'] = 10
        plt.rcParams['axes.labelweight'] = 'normal'
        plt.rcParams['lines.linewidth'] = 1
        plt.rcParams['axes.titlesize'] = 'medium'
        plt.rcParams['axes.titleweight'] = 'medium'
        plt.rcParams['legend.edgecolor'] = '#e6e6e6'
        plt.rcParams['legend.facecolor'] = '#ffffff'

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)

        return (fig, ax)