# Bandit Visualization Documentation
_IN PROGRESS_

This Bandit Visualization module provides an easy-to-use library for implementing and visualizing various Bandit algorithms and environments in machine learning. If you are looking for the following, this library is not for you:
- You want something fast and efficient,
- You want a tool to run very large simulations

It is good to use if you want to
- Visualize your algorithms in various ways
- Easily add new algorithms to the existing ones (fully in python and numpy)


## Usage
The library is implemented in python3. This library is dependent also on the following modules, and you must have them installed to run this:
- yaml (text parsing)
- numpy (math)
- scipy (stats)
- matplotlib (creating graphs)

### Minilanguage Syntax
### Example Files

## How it Works
The *Build* folder countains five sub-folders:
- Core: Underlying Bandit algorithms and environment
- Parse: Take a user input file (see minilanguage syntax) and builds a dictionary of values
- DataGen: Runs the simulations to create external data folders
- Plot: Makes plots and animations
- Formatting: extraneous tools that don't fit anywhere (TODO move this thing somewhere else)

Here is an overview of what the program does:
- The user inputs a file using `python3 run.py user_file.txt` from the command line. `run.py` is the general process manager that calls the appropriate functions when necessary
- The *user_file* is passed to the *text_parse* module which uses YAML to convert the user input into a rudimentary dictionary. This dictionary is passed to a dictionary checker which checks general consistency and establishes some defaults.
- Now that the dictionary is finished, it will no longer be modified. It is passed as an argument to the various functions in the *DataGen* module, depending on the type of data that is desired, then passed to the *Plot* module to make various plots. *Histogram* and *Variable* plots depend on generated or existing data to build the plots.
- For animations, the bandit is run inline using an update function, without generating external data.

#### Making Histograms - `Histogram`
#### Making Variable Plots - `Variable`
#### Making Animations - `Visualize`

## Further Details

### Overall File Structure
_(note: the current file structure is temporary and bound to change)_

### The _Build_ Directory
#### Build/Core
#### Build/Parse
#### Build/DataGen
#### Build/Plot
#### Multiprocessor Rules


### Notes
The critical importance of core_dict
    everything is stored here; during run.py, it is made by calling Parse on some input file
    once the core_dict is made, you NEVER change it; if you need a local version make a deepcopy
    also, you can't add anything to it; all additions etc. should be done during Parse or dictCheck
        since all information is stored here, this is sufficient to do anything desired, in theory
    after the core_dict is made, you can pass it around to various functions
        DataGen functions use the core dict to make data files
        Plot functions use the core dict and data files to make plots
            Animate functions use the core dict to make animations
    the efficiency of this paradigm is that it allows various functions to operate completely independently of each other!
        this makes process management trivial; very few checks are needed (only using join() to make sure data is done before making a plot, etc)
    all communication between DataGen and Plot functions is done by reading and writing to text files; this is described in more detail under Data generation / saving procedure

sub_dict notation:  // explain notation used in general
    sub_dict is some sub dictionary of core_dict

Processes, opening subprocesses, mac limitations, etc.
    all graphical processes must be in main
    all code data generation must be a subprocess
    static graphic generation must wait until all data subprocesses are done
    no writing can be done in a BuildData file; opened in different process and islated

Data generation / saving procedure
    file system / data saving (timestamped)
    file creation rules
    file writing rules
        only open when writing
        always use append
        writing with newlines

Output file procedure

interface.py and run.py
Outline general code structure