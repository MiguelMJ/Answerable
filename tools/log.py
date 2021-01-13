"""Log Tool for Answerable

This file contains the functions used to log control data and debug messages
in a unified format.
"""

import re
import sys

from tools.displayer import bold, red, fg

_logs = []  # list of file handlers
_ansire = re.compile("\\033\[[^m]+m")  # ansi escape sequences


def _strip_ansi(msg):
    """Strip ansi escape sequences"""

    return re.sub(_ansire, "", msg)


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


def abort(who, msg, *argv):
    """Print an error message and aborts execution"""

    advice = False
    if sys.stderr not in _logs:
        add_stderr()
        advice = True
    log(who, fg(msg, red), *argv)
    if advice:
        lognames = ", ".join([fh.name for fh in _logs if fh is not sys.stderr])
        print("Full log in", lognames, file=sys.stderr)
    close_logs()
    exit()


def log(who, msg, *argv):
    """Print to logs a formatted message"""

    who2 = "[" + who + "] "
    textf = who2 + _strip_ansi(msg.format(*argv))
    texts = bold(who2) + msg.format(*argv)
    for f in _logs:
        if f is sys.stderr:
            print(texts, file=f)
            sys.stderr.flush()
        else:
            print(textf, file=f)
