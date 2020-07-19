"""
Utilities to help with debugging and other
missing functionalities.

"""
__all__ = (
    'debug',
    'clamp',
)

from datetime import datetime


LOG_FILE = "game.log"


with open(LOG_FILE, "w") as fh:
    fh.write("")


def debug(msg):
    with open(LOG_FILE, "a") as fh:
        tpl = "[{:%Y-%m-%d %H:%M:%S}] DEBUG - {}\n".format(
            datetime.now(), msg)
        fh.write(tpl)


def clamp(val, lower, upper):
    # NOTE: This is an approximation of the clamp built-in function for
    # GDScript. Perhaps there is Python Math lib equivalent that returns
    # a number based on upper and lower bounds.
    if val >= lower and val <= upper:
        return val
    if val < lower:
        return lower
    elif val > upper:
        return upper
