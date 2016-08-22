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
        self.n_files = len(core_dict['sim'])
        self.daemon = True
        self.total = core_dict['total_lines']
        self.processes = core_dict['Multiprocess']
    def run(self):
        while True:  # TODO fix this to have a termination
            time.sleep(0.5)
            current = [0] * self.n_files
            try:
                for i in range(self.n_files):
                    with open("{}/data{}.txt".format(self.core_dict['DataFolder'], i), 'r') as file:
                        current[i] += sum(1 for line in file) - 1
            except FileNotFoundError:
                pass
            sys.stdout.write("\r" + " {:2.0f} % complete ".format(sum(current)*100/self.total).center(100, "-"))
            sys.stdout.flush()


def run(**arg_dict):
    core_dict = _checkInput(**arg_dict)
    pool = mp.Pool(core_dict['Multiprocess'], _init_worker)
    core_dict.state()

    try:
        if core_dict['init'] == 'Histogram':
            status = _statusThread(core_dict)
            status.start()
            if not core_dict['InputData']:
                HistData(core_dict, pool)
                pool.close()
                pool.join()
            if core_dict['Animate']:  # TODO in general fix this thing
                while True:
                    try:
                        HistAnimation(core_dict)
                        break
                    except FileNotFoundError:
                        time.sleep(0.3)
            HistPlot(core_dict)
        elif core_dict['init'] == 'Variable':
            status = _statusThread(core_dict)
            status.start()
            if not core_dict['InputData']:
                proc_list = VarData(core_dict)
            _run(proc_list, n_processes)
            VarPlot(core_dict)

        elif core_dict['init'] == 'Visualize':
            if core_dict['visual'] == 'ellipse':
                EllipseAnimation(core_dict)
            elif core_dict['visual'] == 'confidence':
                ConfAnimation(core_dict)
            elif core_dict['visual'] == 'distribution':
                DistAnimation(core_dict)

        print("\n\n" + bcolors.OKGREEN + " Done! ".center(100,"-") + bcolors.ENDC + "\n")

        if core_dict['delete'] or core_dict['DeleteData']:
            path = core_dict['DataFolder']
            for i in range(len(core_dict['sim'])):
                os.remove(path + "/data{}.txt".format(i))
            os.rmdir(path)


    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        print("\r" + " "*150)
        sys.exit("\n\n" + bcolors.FAIL + " Keyboard Interrupt! ".center(100,"-") + bcolors.ENDC + "\n")


