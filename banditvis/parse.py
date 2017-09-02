import sys
import multiprocessing as mp
import re

import numpy as np
import yaml
from datetime import datetime
from pprint import pprint

from .helper import msplit
from .formatting import bcolors
from .defaults import CORE_DEFAULTS

def Parse(user_file, **arg_dict):
    """
    Loads the user_file using YAML and then checks the dictionary for
    consistency. Once Parse is completed, it either exits with errors or
    returns a checked core_dict.
    """

    # Try to load the file and catch YAML syntax errors for nicer formatting
    try:
        # merge the two dicts
        core_dict = CoreDict(yaml.load(open(user_file, 'r')), **arg_dict)
    except yaml.parser.ParserError as e:
        # pull some information out of the ParserError
        location = (str(e).split("\n")[1].split(",")[1] + str(e).split("\n")[1].split(",")[2])[1:]
        e_msg = str(e).split("\n")[2]
        sys.exit(bcolors.FAIL + "\nYAML Syntax Error " + bcolors.ENDC
            + "in {}:\n  - {}\n".format(location, e_msg)
        )
    except yaml.scanner.ScannerError as e:
        # pull some information out of the ScannerError
        location = (str(e).split("\n")[1].split(",")[1]
            + str(e).split("\n")[1].split(",")[2]
            )[1:]
        e_msg = str(e).split("\n")[0]
        sys.exit(bcolors.FAIL + "\nYAML Syntax Error " + bcolors.ENDC
            + "in {}:\n  - {}\n".format(location, e_msg)
            )

    # creates a simulation dictionary list for easier access
    core_dict['sim'] = []
    for sim_key in list(core_dict.keys()):
        if sim_key[:10] == 'Simulation':
            core_dict['sim'].append(CoreDict(core_dict[sim_key]))
            del(core_dict[sim_key])

    # perform the dictionary check, and get the errors
    core_dict, errors = DictCheck(core_dict)

    # if there are errors, print them
    if errors:
        sys.exit(bcolors.FAIL
            + "\n" + " ERROR LIST ".center(100, "-") + "\n" + bcolors.ENDC
            + self.errors + "\n\n")
    else:
        print(bcolors.OKGREEN + "\n" + "No Errors!".center(100, "-") + "\n" + bcolors.ENDC)

    warnings = core_dict.warnings()
    if warnings:
        print(bcolors.WARN
            + "\n" + " WARNING LIST ".center(100, "-") + "\n" + bcolors.ENDC
            + "".join(["- {}\n".format(item) for item in warnings]))
        user_response = input("Press Enter to continue, and <any key> + Enter to abort. ")
        if user_response:
            sys.exit(0)

    else:
        print(bcolors.OKGREEN + "\n" + " No Warnings! ".center(100, "-") + "\n" + bcolors.ENDC)

    # done!
    return core_dict


def DictCheck(core_dict):
    """
    The checking function, uses _check class to perform these checks nicely.

    Defaults are built first, followed by checks based on each init file and
    other specifics. The full list of checking functions with explanations
    can be found in the _check class.
    """
    check = Check(core_dict)
    if core_dict['InputData']:
        check.SimExist('label')
        check.Save()
        check.Title()


    elif core_dict['init'] == 'Variable':
        check.Save()

        check.Conflict('horizon')
        check.Conflict('cycles')
        check.SimExist('label')

        check.Args()
        check.Linecount()
        check.Folder()
        check.Title()


    elif core_dict['init'] == 'Histogram':
        check.Save()

        check.Conflict('horizon')
        check.Conflict('cycles')
        check.SimExist('label')

        check.Bins()
        check.Linecount()
        check.Folder()
        check.Title()


    elif core_dict['init'] == 'Visualize':
        pass


    else:
        sys.exit(bcolors.FAIL
            + '\n\nIf you get this message, something went badly wrong...\n'
            + bcolors.ENDC
        )
    return check.give()


class CoreDict(dict):
    """
    Subclasses dict to change behaviour with missing key (allows setting of defults easily) and
    some other custom methods.
    """
    def __init__(self, in_dict, core_defaults=CORE_DEFAULTS, **arg_dict):
        dict.__init__(self, in_dict)

        # precedence: arg_dict, then core_defaults
        self.default = {**core_defaults, **arg_dict}
        self.ignore = {'InputData', 'DataFolder', 'Animate'}
        self.warning_list = []

    def __missing__(self, key):
        try:
            if key not in self.ignore:
                self.warning_list += ["{} missing, defaulting to '{}'".format(
                    key,
                    self.default[key])
                ]
            return self.default[key]
        except KeyError:
            raise KeyError("CoreDict '{}' key missing in both the dict and the default dict.".format(key))

    def warnings(self):
        return [item for item in list(set(self.warning_list))]

    def state(self):
        print("\n" + " Completed Core Dict ".center(100, "-") + "\n")
        pprint(self)
        print("\n" + " Default Dict ".center(100, "-") + "\n")
        pprint(self.default)
        print("\n" + " End State ".center(100, "-") + "\n")
        return None


class Check:
    """
    A class which checks a dictionary for errors. It contains a large number of
    methods which are convenient / reusable when parsing dictionary objects, and also custom methods
    to do variable formatting.

    Positional Arguments:
        * core_dict: a core_dict or dict-like object
    Attributes:
        * core_dict: the core_dict
        * errors: a list of errors
    Methods:
        * give(): returns the core_dict and a formatted of error string
        * Visual(name): (Currently doesn't do anything)
        * Conflict(name): checks for conflict / multiple declarations of 'name'
        * Exist(name): checks if name exists in the dict
        * SimExist(name): checks if name exists in every simulation sub dictionary
        * Save(): checks for the save title, as well as the save output folder
        * Bins(): figure out appropriate bin allocation for histogram plots
        * Args(): check the args for consistency / proper declaration
        * Folder(): creates a data_folder name and prepends the path to it
        * Linecount(): determines how many lines will be printed to data files
        * Title(): creates a title if none exists and formats an existing one
    """

    def __init__(self, core_dict):
        self.core_dict = core_dict
        self.errors = []


    def give(self):
        return (self.core_dict, "\n".join(set(self.errors)))  # removes repeats from self.errors


    def Visual(self, name):
        if core_dict['visual'] == 'confidence':
            pass
        elif core_dict['visual'] == 'ellipse':
            pass
        elif core_dict['visual'] == 'distribution':
            pass
        else:
            pass


    def Conflict(self, name):
        """
        Checks if 'name' exists in the sim dictionaries and in the overall
        dictionary; looks for conflict / multiple declarations of name. If
        there are no errors, it moves every instance of the declaration to
        the simulation subdictionaries for easier access later.
        """
        checklist = \
            {'low_{}'.format(name) : [False] * len(self.core_dict['sim']),
            'top_{}'.format(name) : [False]}

        if name in self.core_dict.keys():
            checklist['top_{}'.format(name)] = True

        for i, sim_dict in enumerate(self.core_dict['sim']):
            if name in sim_dict.keys():
                checklist['low_{}'.format(name)][i] = True

        if not checklist['top_{}'.format(name)]:
            cntr = 0
            for item in checklist['low_{}'.format(name)]:
                if not item:
                    cntr += 1
            if cntr != 0:
                self.errors += ["- ({0}) was not declared at the top level, and you are missing a"
                    " ({0}) declaration in ({1}) simulation(s)".format(name, cntr)]
        else:
            cntr = 0
            for item in checklist['low_{}'.format(name)]:
                if item:
                    cntr += 1
            if cntr != 0:
                self.errors += ["- ({0}) was declared at the top level, but "
                "you have ({0}) declarations in ({1}) simulation(s).".format(
                    name, cntr)]
            else:
                for sim_dict in self.core_dict['sim']:
                    sim_dict['{}'.format(name)] = \
                        self.core_dict['{}'.format(name)]
                del self.core_dict['{}'.format(name)]
        return None


    def Exist(self, name):
        """
        Checks if 'name' exists in the core_dict
        """
        if name not in self.core_dict.keys():
            self.errors += ["- You are missing a top-level ({}) declaration.".format(
                name)]
        else:
            pass
        return None


    def SimExist(self, name):
        """
        Checks if 'name' exists in every single simulation sim_dictionary, and
        adds an error if it doesn't
        """
        checklist = {'low_{}'.format(name) : [False] * len(self.core_dict['sim'])}
        for i, sim_dict in enumerate(self.core_dict['sim']):
            if name in sim_dict.keys():
                checklist['low_{}'.format(name)][i] = True
        if (checklist['low_{}'.format(name)]
            != [True] * len(self.core_dict['sim'])):
            self.errors += ["- You are missing at least one simulation ({}) declaration.".format(
                name)]
        return None


    def Save(self):
        """
        Checks the save format for .pdf or .png. It returns an eror otherwise.
        """
        if (not self.core_dict['PlotSave'].endswith(".pdf")
            and not self.core_dict['PlotSave'].endswith(".png")):
            self.errors += ["- PlotSave: You can only save a plot as a '.pdf' or '.png'. PDF is "
                "the recommended file type for image quality."]
        if self.core_dict.default['out']:
            self.core_dict['PlotSave'] = self.core_dict.default['out'] + "/" + self.core_dict['PlotSave']
            self.core_dict.default['PlotSave'] = self.core_dict.default['out'] + "/" + self.core_dict.default['PlotSave']
        return None


    def Bins(self):
        """
        Determines how many bins the histogram should have based on the proper-
        ties of the bandit.
        """
        self.core_dict['bins'] = []
        for sim_dict in self.core_dict['sim']:
            if sim_dict['Bandit']['ArmList'][0][0] == 'Linear':
                mean_list = [np.inner(arm[1], sim_dict['Bandit']['MeanVector'])
                    for arm in sim_dict['Bandit']['ArmList']]
            else:
                mean_list = [arm[1] for arm in sim_dict['Bandit']['ArmList']]
            self.core_dict['bins'].append(np.amax(
                mean_list - np.amin(mean_list)) * sim_dict['horizon'])
        return None


    def Args(self):
        """
        When using the Variable class, args can be declared in multiple ways.
        This builds a single list of args out of the inputs to be used later.
        """
        checklist = {'linspace': False, 'args': False}
        if ('domain' in self.core_dict['Var'].keys()
            and 'samples' in self.core_dict['Var'].keys()):
            checklist['linspace'] = True

        if 'arg_list' in self.core_dict['Var'].keys():
            checklist['args'] = True

        if checklist['linspace'] and checklist['args']:
            self.errors += ["- Declare either (domain and samples) or (args), not both."]

        elif not checklist['linspace'] and not checklist['args']:
            self.errors += ["- You must declare either (domain and samples) or (args)."]
        else:
            try:
                self.core_dict['arg_list'] = np.linspace(
                    self.core_dict['Var']['domain'][0],
                    self.core_dict['Var']['domain'][1],
                    self.core_dict['Var']['samples'])
            except KeyError:
                pass
        return None


    def Folder(self):
        """
        Additional changes to be done after checking
        """
        self.core_dict.default.setdefault('DataFolder', "{}".format(
            datetime.strftime(datetime.now(), '%Y-%m-%d %H_%M_%S')))
        if self.core_dict.default['data']:
            self.core_dict.default['DataFolder'] = self.core_dict.default['data'] + "/" + self.core_dict.default['DataFolder']
        return None


    def Linecount(self):
        if self.core_dict['init'] == 'Histogram':
            self.core_dict['total_lines'] = sum(sim_dict['cycles'] for sim_dict in self.core_dict['sim'])
        elif self.core_dict['init'] == 'Variable':
            self.core_dict['total_lines'] = len(self.core_dict['arg_list']) * len(self.core_dict['sim'])
        return None


    def Title(self):
        if not self.core_dict['PlotTitle']:
            self.core_dict['PlotTitle'] = msplit(self.core_dict['PlotSave'], "/", ".")[-1] + "\n"
        else:
            self.core_dict['PlotTitle'] += "\n"

        return None
