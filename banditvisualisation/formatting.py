class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
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
    sequential1 = ['Blues', 'Greens', 'Reds', 'BuGn',
        'BuPu','GnBu', 'Greys', 'Oranges',
        'OrRd','PuBu', 'PuBuGn', 'PuRd',
        'Purples', 'RdPu', 'YlGn', 'YlGnBu']
    sequential2 = ['afmhot', 'autumn', 'bone', 'cool',
        'copper', 'gist_heat', 'gray', 'hot',
        'pink', 'spring', 'summer', 'winter']