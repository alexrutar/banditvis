import multiprocessing as mp
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


def run():
    core_dict = _getInput()
    n_processes = core_dict['Multiprocess']
    # -------------------------------------------------------------------------
    print("\n\n--Completed core_dict--\n\n")
    pprint(core_dict)
    print("--\n\n")
    # -------------------------------------------------------------------------

    if core_dict['init'] == 'Histogram':
        if not core_dict['InputData']:
            proc_list = HistData(core_dict)
        if core_dict['Animate']:
            time.sleep(1)  # TODO fix so that it doesn't try to access an
            # empty
            HistAnimation(core_dict)

        # hacky pool-like behaviour; I'm not the biggest fan but it works,
        # unlike multiprocessing.pool!
        _run(proc_list, n_processes)

        HistPlot(core_dict)

    elif core_dict['init'] == 'Variable':
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



