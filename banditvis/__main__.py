"""
Entry point for the banditvis script installed along with this package.


Usage:
    banditvis [options] input
    banditvis -V | --version
    banditvis -h | --help

positional arguments:
  input                     The path to your .txt input file.

optional arguments:
  -D --delete               Delete intermediate data files.
  --data=<directory>        The path to the data directory, defaults to the
                              current directory.
  --out=<directory>         The path to the output location, defaults to the
                              current directory.
"""

from .manager import run
import time
import sys

usage = '\n\n\n'.join(__doc__.split('\n\n\n')[1:])
def get_args():
    """
    Command line argument parser. Parses the arguments
    """

    parser = argparse.ArgumentParser(prog='banditvis', usage=usage)
    parser.add_argument("input",
        help="The path to your .txt input file.")
    parser.add_argument("--data", nargs='?',
        help="The path to the data directory, defaults to the current directory.")
    parser.add_argument("--out", nargs='?',
        help="The path to the output location, defaults to the current directory.")
    parser.add_argument("-D", "--delete", action='store_true',
        help="Delete intermediate data files.")
    args = parser.parse_args()
    return vars(args)

def main():
    run(**get_args())

if __name__ == "__main__":
    main()

