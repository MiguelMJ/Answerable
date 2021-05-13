"""Log Tool for Answerable

This file contains the functions used to log control data and debug messages
in a unified format.
"""

import re
import sys
import inspect

from tools.displayer import bold, red, magenta, fg

_logs = []  # list of file handlers
_ansire = re.compile("\\033\[[^m]+m")  # ansi escape sequences


def _strip_ansi(msg):
    """Strip ansi escape sequences"""

    return re.sub(_ansire, "", msg)


def _get_caller():
    frm = inspect.stack()[2]
    return inspect.getmodule(frm[0]).__name__


def add_stderr():
    """Add the stderr to the log file handlers"""

    _logs.append(sys.stderr)


def add_log(logfile):
    """Open a new file and add it to the log file handlers"""

    _logs.append(open(logfile, "w"))


def close_logs():
    """Close all log file handlers."""

    for f in _logs:
        if f is not sys.stderr:
            f.close()


def advice_message():
    """Returns the advice of where to find the full logs"""
    lognames = ", ".join([fh.name for fh in _logs if fh is not sys.stderr])
    return "Full log in " + lognames


def abort(msg, *argv):
    """Print an error message and aborts execution"""

    if sys.stderr not in _logs:
        add_stderr()
    log(fg(msg, red), *argv, who=_get_caller())
    print_advice()
    close_logs()
    exit()


def warn(msg, *argv):
    """Print an error message and aborts execution"""
    err_off = sys.stderr not in _logs
    if err_off:
        add_stderr()
    log(fg(msg, magenta), *argv, who=_get_caller())
    _logs.pop()


def print_advice():
    """Print where to find the full log if necessary"""

    if sys.stderr not in _logs:
        print(advice_message(), file=sys.stderr)


def log(msg, *argv, **kargs):
    """Print to logs a formatted message"""

    who = kargs["who"] if "who" in kargs else _get_caller()
    who = f"[{who}] "
    textf = who + _strip_ansi(msg.format(*argv))
    texts = bold(who) + msg.format(*argv)
    for f in _logs:
        if f is sys.stderr:
            print(texts, file=f)
            sys.stderr.flush()
        else:
            print(textf, file=f)
