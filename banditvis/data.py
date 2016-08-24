import copy
import os
import numpy as np
from .simulation import ReMapSim
from pprint import pprint
import time

def _fix_vars(obj, variable):
    """
    Recursively searches the nested sim dict structure, and attempts to find
    every instance of '&&', replace it with some variable, and evaulate that
    string. It does this by recursively building a copy of the object if it
    contains dict or list substructures. Note that this function will not
    search in any structures other than lists or dicts.
    """
    if isinstance(obj, dict):
        return {key: _fix_vars(val, variable) for key, val in obj.items()}
    elif isinstance(obj, list):
        return [_fix_vars(key, variable) for key in obj]
    elif isinstance(obj, str):
        if '&&' in obj:
            return eval(obj.replace("&&", str(variable)))
        else:
            return obj
    return obj

def HistData(i, sim_dict, data_folder="."):
    """
    Generates Histogram data.

    Runs the bandit algorithms to create files containing regret data for each
    element of core_dict['sim']
        * builds a temporary dictionary which is a deep copy of the correspon-
            ding simulation dictionary
        * uses ReMapSim to build a Simulation object
        * runs that Simulation object using runHist
        * saves that data in the specified folder
    """
    file_name = "{}/data{}.txt".format(data_folder, i)
    temp_dict = copy.deepcopy(sim_dict)
    ReMapSim(temp_dict)
    sim = temp_dict['Simulation']

    sim.runHist(
        temp_dict['horizon'],
        temp_dict['cycles'],
        file_name)

    return None


def VarData(i, sim_dict, data_folder=".", iter_list = []):
    """
    Generates Variable data.

    VarData runs the bandit algorithms to create files containing regret data
    for each element of core_dict['sim']. It:
        * builds a temporary dictionary which is a deep copy of the correspond-
            ing simulation dictionary
        * uses ReMapSim to build a Simulation object
        * runs that Simulation object using runVar
        * saves the output data to sequentially generated save files

    The inner loop works as follows:
        * temp_dict is made as a copy
        * every instance of '#' is replaced with num
        * the bandit algorithm is run using the replaced string
    """
    for num in iter_list:  # now num is the variable
        temp_dict = _fix_vars(sim_dict, num)

        ReMapSim(temp_dict)
        sim = temp_dict['Simulation']

        file_name = "{}/data{}.txt".format(data_folder, i)
        sim.runVar(
            temp_dict['horizon'],
            temp_dict['cycles'],
            file_name
        )

    return None