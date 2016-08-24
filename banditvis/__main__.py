"""
Entry point for the banditvis script installed along with this package.


Usage:
    banditvis [options] input
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
"""
from . import __version__
from .manager import run
import time
import sys
import argparse

def get_usage():
    return '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
def get_args():
    """
    Command line argument parser. Parses the arguments
    """

    parser = argparse.ArgumentParser(prog='banditvis')#, usage=usage)
    parser.add_argument("input",
        help="The path to your .txt input file.")
    parser.add_argument("--data", nargs='?',
        help="The path to the data directory, defaults to the current directory.")
    parser.add_argument("--out", nargs='?',
        help="The path to the output location, defaults to the current directory.")
    parser.add_argument("-D", "--delete", action='store_true',
        help="Delete intermediate data files.")
    if ("-h" or "--help") in sys.argv[1:]:
        print(get_usage())
        sys.exit(0)
    elif "-V" or "--version" in sys.argv[1:]:
        print("banditvis ({}) -- installed at {}".format(__version__, "/".join(__file__.split("/")[:-1])))
        sys.exit(0)
    else:
        return args

def main():
    run(**get_args())

if __name__ == "__main__":
    main()

