# TODO: Tests and comments
def set(value, flag):
    return value | flag


def isset(value, flag):
    return (value & flag) == flag


def unset(value, flag):
    return value & ~flag
