import argparse

# parser = argparse.ArgumentParser(description="A command line interface for the banditvis module.")

def get_args():
    parser = argparse.ArgumentParser(prog='banditvis')
    parser.add_argument("input",
        help="The path to your .txt input file.")
    parser.add_argument("-d", "--data", nargs='?',
        help="The path to the data directory, defaults to the current directory.")
    parser.add_argument("-o", "--out", nargs='?',
        help="The path to the output location, defaults to the current directory.")
    args = parser.parse_args()
    print(vars(args))
    return vars(args)