import sys

import numpy as np
import yaml
from datetime import datetime

from .formatting import bcolors


def Parse(user_file):
    """
    Loads the user_file using YAML and then checks the dictionary for
    consistency. Once Parse is completed, it either exits with errors or
    returns a checked core_dict.
    """

    # Try to load the file and catch YAML syntax errors for nicer formatting
    try:
        initial_dict = yaml.load(open(user_file, 'r'))
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
    initial_dict['sim'] = []
    for sim_key in list(initial_dict.keys()):
        if sim_key[:10] == 'Simulation':
            initial_dict['sim'].append(initial_dict[sim_key])
            del(initial_dict[sim_key])

    # perform the dictionary check, and get the errors
    core_dict, errors = DictCheck(initial_dict)

    # if there are errors, print them
    if errors:
        sys.exit(bcolors.FAIL
            + "\n+" + "ERROR LIST".center(100, "-") + "+\n" + bcolors.ENDC
            + self.errors + "\n\n")
    else:
        print(bcolors.OKGREEN
            + "\n" + "".center(100, "=")
            + "\n" + "".center(100, "=")
            + "\n" + bcolors.ENDC)

    # done!
    return core_dict


def DictCheck(initial_dict):
    """
    The checking function, uses _check class to perform these checks nicely.

    Defaults are built first, followed by checks based on each init file and
    other specifics. The full list of checking functions with explanations
    can be found in the _check class.
    """
    _defaults(initial_dict)

    check = _check(initial_dict)
    if initial_dict['InputData']:
        check.SimExist('label')
        check.Save()
        check.Title()
    elif initial_dict['init'] == 'Variable':
        check.Save()
        check.Title()

        check.Conflict('horizon')
        check.Conflict('cycles')
        check.SimExist('label')

        check.Args()
    elif initial_dict['init'] == 'Histogram':
        check.Save()
        check.Title()

        check.Conflict('horizon')
        check.Conflict('cycles')
        check.SimExist('label')

        check.Bins()
    elif initial_dict['init'] == 'Visual':
        pass
    else:
        sys.exit(bcolors.FAIL
            + '\n\nIf you get this message, something wend badly wrong...\n'
            + bcolors.ENDC)
    return check.give()


def _defaults(initial_dict):
    """
    Builds some default values in the initial_dict.

    This is going ot be fixed soon...
    """
    initial_dict.setdefault('InputData', False)
    if (initial_dict['init'] == 'Histogram'
        or initial_dict['init'] == 'Variable'):
        # data folder to save data files in; uses a timestamp for a label
        if not initial_dict['InputData']:
            initial_dict.setdefault('data_folder',
                "Data/{}".format(
                    initial_dict['init'][:4]
                    + " "
                    + datetime.strftime(
                        datetime.now(), '%Y-%m-%d %H_%M_%S')))
        else:
            initial_dict.setdefault('data_folder',
                "Data/{}".format(initial_dict['InputData']))
        initial_dict.setdefault('Animate', False)
        initial_dict.setdefault('FPS', 20)
        initial_dict.setdefault('PlotSave', "temp.pdf")
    if initial_dict['init'] == 'Variable':
        initial_dict.setdefault('ylabel', 'Regret')
        initial_dict.setdefault('xlabel', ' ')
    for sub_dict in initial_dict['sim']:
        if initial_dict['init'] == 'Visualize':
            initial_dict.setdefault('FPS', 20)
            sub_dict.setdefault('NoAxesTick', False)
            sub_dict.setdefault('HelpLines', True)
            sub_dict.setdefault('FPS', 20)
            sub_dict.setdefault('LevelCurves', True)
        if not initial_dict['InputData']:
            if sub_dict['Bandit']['ArmList'][0][0] == 'Linear':
                sub_dict.setdefault('Normalized', False)
    return None


class _check:
    """
    A class which checks a dictionary for errors. It contains a large number of
    methods which are convenient / reusable when parsing dictionary objects.

    """

    def __init__(self, initial_dict):
        self.initial_dict = initial_dict
        self.errors = ""

    def give(self):
        return (self.initial_dict, self.errors)

    def Conflict(self, name):
        """
        Checks if 'name' exists in the sim dictionaries and in the overall
        dictionary; looks for conflict / multiple declarations of name. If
        there are no errors, it moves every instance of the declaration to
        the simulation subdictionaries for easier access later.
        """
        checklist = \
            {'low_{}'.format(name) : [False] * len(self.initial_dict['sim']),
            'top_{}'.format(name) : [False]}

        if name in self.initial_dict.keys():
            checklist['top_{}'.format(name)] = True

        for i, sub_dict in enumerate(self.initial_dict['sim']):
            if name in sub_dict.keys():
                checklist['low_{}'.format(name)][i] = True

        if not checklist['top_{}'.format(name)]:
            cntr = 0
            for item in checklist['low_{}'.format(name)]:
                if not item:
                    cntr += 1
            if cntr != 0:
                self.errors += ("\n- ({0}) was not declared at the top level, "
                    "and you are missing a ({0}) declaration in ({1}) "
                    "simulation(s)".format(name, cntr))
        else:
            cntr = 0
            for item in checklist['low_{}'.format(name)]:
                if item:
                    cntr += 1
            if cntr != 0:
                self.errors += ("\n- ({0}) was declared at the top level, but "
                "you have ({0}) declarations in ({1}) simulation(s).".format(
                    name, cntr))
            else:
                for sub_dict in self.initial_dict['sim']:
                    sub_dict['{}'.format(name)] = \
                        self.initial_dict['{}'.format(name)]
                del self.initial_dict['{}'.format(name)]
        return None


    def SimExist(self, name):
        """
        Checks if 'name' exists in every single simulation sub_dictionary, and
        adds an error if it doesn't
        """
        checklist = \
            {'low_{}'.format(name) : [False] * len(self.initial_dict['sim'])}
        for i, sub_dict in enumerate(self.initial_dict['sim']):
            if name in sub_dict.keys():
                checklist['low_{}'.format(name)][i] = True
        if (checklist['low_{}'.format(name)]
            != [True] * len(self.initial_dict['sim'])):
            self.errors += ("\n- You are missing at least one simulation ({}) "
                "declaration.".format(name))
        return None


    def Save(self):
        """
        Checks the save format for .pdf or .png. It returns an error otherwise.
        """
        self.initial_dict.setdefault('PlotSave', 'temp.pdf')
        if ('.pdf' not in self.initial_dict['PlotSave'][-4:]
            and '.png' not in self.initial_dict['PlotSave'][-4:]):
            self.errors += ("\n- PlotSave: You can only save a plot as a "
                "'.pdf' or '.png'. PDF is the recommended file type for image "
                "quality reasons.")
        self.initial_dict['PlotSave'] = \
            'Output/' + self.initial_dict['PlotSave']
        return None


    def Title(self):
        """
        Checks if a title exists; if one desn't it generates one from the file
        name, and if one does it adds a newline below for formatting.
        """
        self.initial_dict.setdefault('PlotTitle', False)
        if not self.initial_dict['PlotTitle']:
            self.initial_dict['PlotTitle'] = \
                self.initial_dict['PlotSave'].split("/")[-1].split(".")[0] \
                + "\n"
        else:
            self.initial_dict['PlotTitle'] += "\n"
        return None


    def Bins(self):
        """
        Determines how many bins the histogram should have based on the proper-
        ties of the bandit.
        """
        self.initial_dict['bins'] = []
        for sub_dict in self.initial_dict['sim']:
            if sub_dict['Bandit']['ArmList'][0][0] == 'Linear':
                mean_list = [np.inner(arm[1], sub_dict['Bandit']['MeanVector'])
                    for arm in sub_dict['Bandit']['ArmList']]
            else:
                mean_list = [arm[1] for arm in sub_dict['Bandit']['ArmList']]
            self.initial_dict['bins'].append(np.amax(
                mean_list - np.amin(mean_list)) * sub_dict['horizon'])
        return None


    def Args(self):
        """
        When using the Variable class, args can be declared in multiple ways.
        This builds a single list of args out of the inputs to be used later.
        """
        checklist = {'linspace': False, 'args': False}
        if ('domain' in self.initial_dict['Var'].keys()
            and 'samples' in self.initial_dict['Var'].keys()):
            checklist['linspace'] = True

        if 'arg_list' in self.initial_dict['Var'].keys():
            checklist['args'] = True

        if checklist['linspace'] and checklist['args']:
            self.errors += ("\n- Declare either (domain and samples) or (args)"
                ", not both.")

        elif not checklist['linspace'] and not checklist['args']:
            self.errors += ("\n- You must declare either (domain and samples) "
                "or (args).")
        else:
            try:
                self.initial_dict['arg_list'] = np.linspace(
                    self.initial_dict['Var']['domain'][0],
                    self.initial_dict['Var']['domain'][1],
                    self.initial_dict['Var']['samples'])
            except KeyError:
                pass

        # calculate the total number of operations that the Variable class is
        # going to run through
        t_ops = 0
        for sub_dict in self.initial_dict['sim']:
            t_ops += len(self.initial_dict['arg_list'])
        for sub_dict in self.initial_dict['sim']:
            sub_dict['total_ops'] = t_ops
        self.initial_dict['op_n'] = 0

        return None
