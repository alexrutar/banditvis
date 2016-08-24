"""
The manager module for the command line tools. It does multiprocess management, as well as
"""
import multiprocessing as mp
import threading as th
from pprint import pprint
import sys
import time
import signal
import os

from .parse import Parse
from .plot import *
from .data import *
from .animation import *
from .formatting import bcolors

def _checkInput(**arg_dict):
    """
    Gets the input from the user commmand and checks it for potential errors.
    """
    if arg_dict['input'].endswith('.txt'):
        pass
    else:
        sys.exit("ERROR: You need to input a .txt file.")
    try:
        input_file = arg_dict['input']
        del(arg_dict['input'])
        core_dict = Parse("{}".format(input_file), **arg_dict)
    except FileNotFoundError:
        sys.exit("ERROR: The file '{}' you tried to input doesn't exist in the current directory.".format(input_file))
    return core_dict

def _init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

class _statusThread(th.Thread):
    def __init__(self, core_dict):
        super(_statusThread, self).__init__()
        self.core_dict = core_dict
        self.daemon = True
    def run(self):
        n_files = len(self.core_dict['sim'])
        current = [0] * n_files
        finished = 0
        total = self.core_dict['total_lines']
        while finished != total:  # TODO fix this to have a termination
            time.sleep(0.5)
            for i in range(n_files):
                try:
                    with open("{}/data{}.txt".format(self.core_dict['DataFolder'], i), 'r') as file:
                        current[i] = sum(1 for line in file) - 1
                except FileNotFoundError:
                    pass
            finished = sum(current)
            sys.stdout.write("\r" + " {:2.0f} % complete ".format(finished*100/total).center(100, "-"))
            sys.stdout.flush()


def run(**arg_dict):
    core_dict = _checkInput(**arg_dict)
    pool = mp.Pool(core_dict['Multiprocess'], _init_worker)
    # ----------------------------------------------------------------------------------------------
    core_dict.state()  # displays the core_dict

    try:
        if core_dict['init'] == 'Histogram':
            os.mkdir(core_dict['DataFolder'])
            status = _statusThread(core_dict)
            status.start()
            if not core_dict['InputData']:
                pool.starmap(HistData, [(i, sim_dict, core_dict['DataFolder'])
                    for i, sim_dict in enumerate(core_dict['sim'])])
                pool.close()
                pool.join()
                if core_dict['Animate']:  # TODO in general fix this thing
                    while True:
                        try:
                            HistAnimation(core_dict)
                            break
                        except FileNotFoundError:
                            time.sleep(0.3)
            else:
                pass
            HistPlot(core_dict)

        elif core_dict['init'] == 'Variable':
            os.mkdir(core_dict['DataFolder'])
            status = _statusThread(core_dict)
            status.start()
            if not core_dict['InputData']:
                pool.starmap(VarData, [(i, sim_dict, core_dict['DataFolder'], core_dict['arg_list'])
                    for i, sim_dict in enumerate(core_dict['sim'])])
                pool.close()
                pool.join()
            else:
                pass
            VarPlot(core_dict)

        elif core_dict['init'] == 'Visualize':
            if core_dict['visual'] == 'ellipse':
                EllipseAnimation(core_dict)
            elif core_dict['visual'] == 'confidence':
                ConfAnimation(core_dict)
            elif core_dict['visual'] == 'distribution':
                DistAnimation(core_dict)

        # ------------------------------------------------------------------------------------------
        # POST PROCESSING
        # ------------------------------------------------------------------------------------------

        print("\n\n" + bcolors.OKGREEN + " Done! Saved to {} ".format(core_dict['PlotSave']).center(100,"-") + bcolors.ENDC + "\n")

        if core_dict['delete'] or core_dict['DeleteData']:
            path = core_dict['DataFolder']
            for i in range(len(core_dict['sim'])):
                os.remove(path + "/data{}.txt".format(i))
            os.rmdir(path)


    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        print("\r" + " "*150)
        print("\n\n" + bcolors.FAIL + " Keyboard Interrupt! ".center(100,"-") + bcolors.ENDC + "\n")
        sys.exit(1)


