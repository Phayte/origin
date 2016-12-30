"""
This module is a collection of functions most commonly supported by other
language for convenience to reduce code clutter in the main logic of other
functions.
    * is_none: Similar to ISNULL(sql) or ??(C#), takes a list
               of parameters and will return the first non-None parameter
"""


def is_none(*args):
    if len(args) == 0:
        return None

    for arg in args:
        if arg is not None:
            return arg

    return None


def is_exit(obj):
    return obj.destination
