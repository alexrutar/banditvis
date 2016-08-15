import multiprocessing as mp
import threading as th
from pprint import pprint
import sys
import time

from .parse import Parse
from .plot import *
from .data import *
from .animation import *

def _getInput():
    """
    Gets the input from the user commmand and checks it for potential errors.
    """
    try:
        if sys.argv[1].endswith('.txt'):
            input_file = sys.argv[1]
        else:
            sys.exit("ERROR: You need input a .txt file.")
    except IndexError:
        sys.exit("ERROR: You need to specify a file.")
    try:
        core_dict = Parse("{}".format(input_file))
    except FileNotFoundError:
        sys.exit("ERROR: The file you tried to input doesn't exist in the "
            "current directory.")
    return core_dict


class _managerThread(th.Thread):
    def __init__(self, proc_list, n_processes):
        super(_statusThread, self).__init__()


def _run(proc_list, n_processes):
    def _chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
    for sub_proc in _chunks(proc_list, n_processes):
        for process in sub_proc:
            process.start()
        for process in sub_proc:
            process.join()
    return None

class _statusThread(th.Thread):
    def __init__(self, core_dict):
        super(_statusThread, self).__init__()
        self.core_dict = core_dict
        self.n_files = len(core_dict['sim'])
        self.daemon = True
        self.total = core_dict['total_lines']
    def run(self):
        while True:  # TODO fix this to have a termination
            time.sleep(0.5)
            current = 0
            try:
                for i in range(self.n_files):
                    with open("{}/data{}.txt".format(self.core_dict['DataFolder'],i), 'r') as file:
                        current += sum(1 for line in file) - 1
            except FileNotFoundError:
                pass
            sys.stdout.write("\r--  {} % complete --".format(int(current*100/self.total)))
            sys.stdout.flush()



def run():
    core_dict = _getInput()
    n_processes = core_dict['Multiprocess']
    # ----------------------------------------------------------------------------------------------
    print("\n\nCompleted core_dict\n")
    pprint(core_dict)
    print("--\n\n")
    print("Default Dict\n")
    pprint(core_dict.default)
    print("--\n\n")
    # ----------------------------------------------------------------------------------------------

    if core_dict['init'] == 'Histogram':
        status = _statusThread(core_dict)
        status.start()
        if not core_dict['InputData']:
            proc_list = HistData(core_dict)
        if core_dict['Animate']:  # TODO in general fix this thing
            while True:
                try:
                    HistAnimation(core_dict)
                    break
                except FileNotFoundError:
                    time.sleep(0.3)
        # hacky pool-like behaviour; I'm not the biggest fan but it works, unlike mp.pool!
        _run(proc_list, n_processes)

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



