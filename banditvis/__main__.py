"""
Entry point for the banditvis script installed along with this package.


Usage:
    banditvis [options] input
    banditvis --default=<source>

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
  -v, --verbose         Display additional information.

Other:
  --default=<source>    Source defaults from a specified file.
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
    parser.add_argument("--default", nargs='?',
        help="Source defaults from a specified file.")
    parser.add_argument("-v","--verbose", action='store_true',
        help="Display additional information.")

    # check for certain arguments
    if (("-h" or "--help") in sys.argv[1:]) or (len(sys.argv) == 1):
        print(get_usage())
        sys.exit(0)
    elif ("-V" or "--version") in sys.argv[1:]:
        print("banditvis ({}) -- installed at {}".format(__version__, os.path.dirname(__file__)))
        sys.exit(0)

    # parse the arguments
    else:
        unmod_args = vars(parser.parse_args())
        args = {key:unmod_args[key] for key in unmod_args.keys() if unmod_args[key] is not None}
        if 'default' in args.keys():
            file_name = args['default']
            try:
                with open(file_name, 'r') as file:
                    user_defaults = yaml.load(file)
                with open(os.path.dirname(__file__) + '/user_defaults.pkl', 'wb') as handle:
                    pickle.dump(user_defaults, handle)
                if args['verbose']:
                    print("Successfully loaded default file! Results:\n")
                    pprint(user_defaults)
                    print("\n")
                else:
                    print("Successfully loaded default file!")

                sys.exit(0)
            except FileNotFoundError:
                print("Default file '{}' not found.".format(file_name))
                sys.exit(1)
        # remove any None values
        return args

def main():
    run(**get_args())

if __name__ == "__main__":
    main()

