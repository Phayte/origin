"""
This module is a collection of functions most commonly supported by other
language for convenience to reduce code clutter in the main logic of other
functions.
    * is_none: Similar to ISNULL(sql) or ??(C#), takes a list
               of parameters and will return the first non-None parameter
"""

# TODO: Tests and comments
from evennia.utils import inherits_from


def is_none(*args):
    if len(args) == 0:
        return None

    for arg in args:
        if arg is not None:
            return arg

    return None


def is_exit(obj):
    from typeclasses.exits import Exit
    return obj.destination and inherits_from(obj, Exit)


def is_construct(obj):
    from typeclasses.construct import Construct
    return inherits_from(obj, Construct)


def get_saver_dict(obj, namespace, persist=True):
    if persist:
        attr_handler = obj.attributes
    else:
        attr_handler = obj.nattributes

    if not attr_handler.has(namespace):
        attr_handler.add(namespace, {})
    return attr_handler.get(namespace)
