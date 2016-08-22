import argparse

# parser = argparse.ArgumentParser(description="A command line interface for the banditvis module.")

def safe_save(file_name):
    """Save a plot safely."""
    if file_name.split("/")[-1][:4] == 'temp':
        return file_name
    elif not os.path.isfile(file_name):
        return file_name
    else:
        for i in range(100000):
            if os.path.isfile(file_name.split(".")[0]
                + "{}.".format(i)
                + file_name.split(".")[1]):
                pass
            else:
                return(file_name.split(".")[0]
                    + "{}.".format(i)
                    + file_name.split(".")[1])

def get_args():
    parser = argparse.ArgumentParser(prog='banditvis')
    parser.add_argument("input",
        help="The path to your .txt input file.")
    parser.add_argument("-d", "--data", nargs='?',
        help="The path to the data directory, defaults to the current directory.")
    parser.add_argument("-o", "--out", nargs='?',
        help="The path to the output location, defaults to the current directory.")
    parser.add_argument("-D", "--delete", action='store_true',
        help="Delete intermediate data files.")
    args = parser.parse_args()
    print(vars(args))
    return vars(args)


def msplit(text, *limiters):
    """
    splits 'text' at every occurrence of limiter
    """
    for limit in limiters:
        text = text.replace(limit, '$!!7=4+[4}|[2')
    return text.split('$!!7=4+[4}|[2')