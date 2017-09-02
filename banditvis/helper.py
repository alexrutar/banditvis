import os

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

def msplit(text, *limiters):
    """
    Like split, but separates a string at multiple places.

    Args:
        text: a string that you want to split
        *limiters: strings that you want to split at
    Returns:
        A list of strings

    Examples:

    >>> msplit("example test string here!", 'p', 'g')
    ['exam', 'le test strin', ' here!']

    """
    for limit in limiters:
        text = text.replace(limit, '$!!7=4+[4}|[2')
    return text.split('$!!7=4+[4}|[2')
