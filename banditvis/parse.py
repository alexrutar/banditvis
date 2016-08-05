import re
import sys

import numpy as np
import yaml
from datetime import datetime
from pprint import pprint

from .formatting import bcolors


def Parse(user_file):
    # load the file using YAML and format the error messages nicely
    try:
        core_dict = yaml.load(open(user_file, 'r'))
    except yaml.parser.ParserError as e:
        location = (str(e).split("\n")[1].split(",")[1]
            + str(e).split("\n")[1].split(",")[2]
            )[1:]
        e_msg = str(e).split("\n")[2]
        sys.exit(
            bcolors.FAIL
            + "\nYAML Syntax Error "
            + bcolors.ENDC
            + "in {}:\n  > {}\n".format(location, e_msg)
            )
    except yaml.scanner.ScannerError as e:
        location = (str(e).split("\n")[1].split(",")[1]
            + str(e).split("\n")[1].split(",")[2]
            )[1:]
        e_msg = str(e).split("\n")[0]
        sys.exit(
            bcolors.FAIL
            + "\nYAML Syntax Error "
            + bcolors.ENDC
            + "in {}:\n  > {}\n".format(location, e_msg)
            )

    # creates a simulation dictionary list for easier access
    core_dict['sim'] = []
    for sim_key in list(core_dict.keys()):
        if sim_key[:10] == 'Simulation':
            core_dict['sim'].append(core_dict[sim_key])
            del(core_dict[sim_key])

    errors = DictCheck(core_dict)
    if errors:
        sys.exit(bcolors.FAIL
            + "\n+" + "ERROR LIST".center(100, "-") + "+\n" + bcolors.ENDC
            + errors + "\n\n")
    else:
        print(bcolors.OKGREEN
            + "\n" + "".center(100, "=")
            + "\n" + "".center(100, "=")
            + "\n" + bcolors.ENDC)
    pprint(core_dict)

    return core_dict


def _defaults(core_dict):
    # -------------------------------------------------------------------------

    # DEFAULTS

    # -------------------------------------------------------------------------

    if core_dict['init'] == 'Histogram' or core_dict['init'] == 'Variable':
        # data folder to save data files in; uses a timestamp for a label
        core_dict.setdefault('data_folder',
            "Data/{}".format(core_dict['init'][:4] + " " + datetime.strftime(
                datetime.now(), '%Y-%m-%d %H_%M_%S')))
        core_dict.setdefault('Animate', False)
        core_dict.setdefault('PlotSave', "temp.pdf")
    if core_dict['init'] == 'Variable':
        core_dict.setdefault('ylabel', 'Regret')
        core_dict.setdefault('xlabel', ' ')
    for sub_dict in core_dict['sim']:
        if core_dict['init'] == 'Visualize':
            core_dict.setdefault('FPS', 20)
            sub_dict.setdefault('NoAxesTick', False)
            sub_dict.setdefault('HelpLines', True)
            sub_dict.setdefault('FPS', 20)
        if sub_dict['Bandit']['ArmList'][0][0] == 'Linear':
            sub_dict.setdefault('Normalized', False)
    return None


def DictCheck(core_dict):
    """
    Checks the dictionary for correctness and consistency

    """

    errors = ""

    # -------------------------------------------------------------------------

    # GLOBAL CHECK FUNCTIONS

    # -------------------------------------------------------------------------

    def _checkConflict(name):
        """
        Checks if 'name' exists in the sim dictionaries and in the overall
        dictionary; looks for conflict / multiple declarations of name. If
        there are no errors, it moves every instance of the declaration to the
        simulation subdictionaries for easier access later.
        """
        nonlocal errors, core_dict
        checklist = \
            {'low_{}'.format(name) : [False] * len(core_dict['sim']),
            'top_{}'.format(name) : [False]}

        if name in core_dict.keys():
            checklist['top_{}'.format(name)] = True

        for i, sub_dict in enumerate(core_dict['sim']):
            if name in sub_dict.keys():
                checklist['low_{}'.format(name)][i] = True

        if not checklist['top_{}'.format(name)]:  # if top_horizon isn't declared, low_horizon should be all true
            cntr = 0
            for item in checklist['low_{}'.format(name)]:
                if not item:
                    cntr += 1
            if cntr != 0:
                errors += "\n- ({0}) was not declared at the top level, and you are missing a ({0}) declaration in ({1}) simulation(s)".format(name, cntr)
        else:
            cntr = 0
            for item in checklist['low_{}'.format(name)]:
                if item:
                    cntr += 1
            if cntr != 0:
                errors += "\n- ({0}) was declared at the top level, but you have ({0}) declarations in ({1}) simulation(s).".format(name, cntr)
            else:
                for sub_dict in core_dict['sim']:
                    sub_dict['{}'.format(name)] = core_dict['{}'.format(name)]  # fill in all the sub_dictionaries with 'cycles'
                del core_dict['{}'.format(name)]
        return None


    def _checkSimExist(name):
        """
        Checks if 'name' exists in every single simulation sub_dictionary, and adds an error if it doesn't
        """
        nonlocal core_dict, errors
        checklist = {'low_{}'.format(name) :  [False] * len(core_dict['sim'])}
        for i, sub_dict in enumerate(core_dict['sim']):
            if name in sub_dict.keys():
                checklist['low_{}'.format(name)][i] = True
        if checklist['low_{}'.format(name)] != [True] * len(core_dict['sim']):
            errors += "\n- You are missing at least one simulation ({}) declaration.".format(name)
        return None


    def _checkSave():
        """
        Checks the save format for .pdf or .png
        """
        nonlocal errors, core_dict
        core_dict.setdefault('PlotSave', 'temp.pdf')
        if ('.pdf' not in core_dict['PlotSave'][-4:]
            and '.png' not in core_dict['PlotSave'][-4:]):
            errors += ("\n- PlotSave: You can only save a plot as a '.pdf' or "
                "'.png'. PDF is the recommended file type for image quality "
                "reasons.")
        core_dict['PlotSave'] = 'Output/' + core_dict['PlotSave']
        return None


    def _checkTitle():
        """
        Checks if a title exists; if one desn't it generates one from the file
        name, and if one does it adds a newline below for formatting.
        """
        nonlocal core_dict
        core_dict.setdefault('PlotTitle', False)
        if not core_dict['PlotTitle']:
            core_dict['PlotTitle'] = \
                core_dict['PlotSave'].split("/")[-1].split(".")[0] + "\n"
        else:
            core_dict['PlotTitle'] += "\n"
        return None

    def _evalBins():
        """
        Determines how many bins the histogram should have.
        """
        nonlocal core_dict
        core_dict['bins'] = []
        for sub_dict in core_dict['sim']:
            if sub_dict['Bandit']['ArmList'][0][0] == 'Linear':
                mean_list = [np.inner(arm[1], sub_dict['Bandit']['MeanVector'])
                    for arm in sub_dict['Bandit']['ArmList']]
            else:
                mean_list = [arm[1] for arm in sub_dict['Bandit']['ArmList']]
            core_dict['bins'].append(np.amax(
                mean_list - np.amin(mean_list)) * sub_dict['horizon'])
        return None

    def _checkArgs():
        nonlocal core_dict
        checklist = {'linspace': False, 'args': False}
        if ('domain' in core_dict['Var'].keys()
            and 'samples' in core_dict['Var'].keys()):
            checklist['linspace'] = True

        if 'arg_list' in core_dict['Var'].keys():
            checklist['args'] = True

        if checklist['linspace'] and checklist['args']:
            errors += "\n- Declare either (domain and samples) or (args), not "
            "both."

        elif not checklist['linspace'] and not checklist['args']:
            errors += "\n- You must declare either (domain and samples) or "
            "(args)."
        else:
            try:
                core_dict['arg_list'] = np.linspace(
                    core_dict['Var']['domain'][0],
                    core_dict['Var']['domain'][1],
                    core_dict['Var']['samples'])
                print("hi")
            except KeyError:
                pass
        t_ops = 0
        for sub_dict in core_dict['sim']:
            t_ops += len(core_dict['arg_list'])
        for sub_dict in core_dict['sim']:
            sub_dict['total_ops'] = t_ops
        core_dict['op_n'] = 0

        return None
    # -------------------------------------------------------------------------

    # PERFORM CHECKS

    # -------------------------------------------------------------------------
    _defaults(core_dict)

    if core_dict['init'] == 'Variable':
        _checkSave()
        _checkTitle()

        _checkConflict('horizon')
        _checkConflict('cycles')
        _checkSimExist('label')

        _checkArgs()
    elif core_dict['init'] == 'Histogram':
        _checkSave()
        _checkTitle()

        _checkConflict('horizon')
        _checkConflict('cycles')
        _checkSimExist('label')

        _evalBins()
    elif core_dict['init'] == 'Visual':
        pass
    return errors