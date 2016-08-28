"""
Entry point for the banditvis script installed along with this package.


Usage:
    banditvis [options] input
    banditvis default=<source> [--show]

    banditvis -h | --help
    banditvis -V | --version

Positional:
  input                 The path to your .txt input file.

Optional:
  -D, --delete          Delete intermediate data files.
  --data=<directory>    The path to the data directory, defaults to the
                          current directory.
  --out=<directory>     The path to the output location, defaults to the
                          current directory.

Other:
  default=<source>      Source defaults from a specified file.
  --show                Optional argument for default, prints out the loaded defaults.
"""
from . import __version__
from .manager import run
import time
import sys
import os
import yaml
import argparse
import pickle
from pprint import pprint

def get_usage():
    return '\n\n\n'.join(__doc__.split('\n\n\n')[1:])

def get_args():
    """
    Command line argument parser. Parses the arguments
    """
    # nargs='?' means 0 or 1 argument
    parser = argparse.ArgumentParser(prog='banditvis')
    parser.add_argument("input", nargs='?',
        help="The path to your .txt input file.")
    parser.add_argument("--data", nargs='?',
        help="The path to the data directory, defaults to the current directory.")
    parser.add_argument("--out", nargs='?',
        help="The path to the output location, defaults to the current directory.")
    parser.add_argument("-D", "--delete", action='store_true',
        help="Delete intermediate data files.")

    # check for certain arguments
    if (("-h" or "--help") in sys.argv[1:]) or (len(sys.argv) == 1):
        print(get_usage())
        sys.exit(0)
    elif ("-V" or "--version") in sys.argv[1:]:
        print("banditvis ({}) -- installed at {}".format(__version__, "/".join(__file__.split("/")[:-1])))
        sys.exit(0)
    elif "default" in sys.argv[1]:
        file_name = sys.argv[1].split("=")[1]
        try:
            with open(file_name, 'r') as file:
                user_defaults = yaml.load(file)
            with open(os.path.dirname(__file__) + '/user_defaults.pkl', 'wb') as handle:
                pickle.dump(user_defaults, handle)
            if "--show" in sys.argv[1:]:
                print("Successfully loaded default file! Results:\n")
                pprint(user_defaults)
                print("\n")
            else:
                print("Successfully loaded default file!")

            sys.exit(0)
        except FileNotFoundError:
            print("Default file '{}' not found.".format(file_name))
            sys.exit(1)


    # parse the arguments
    else:
        args = vars(parser.parse_args())
        # remove any None values
        return {key:args[key] for key in args.keys() if args[key] is not None}

def main():
    run(**get_args())

if __name__ == "__main__":
    main()

