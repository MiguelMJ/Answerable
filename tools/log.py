import re
import sys

from tools.displayer import bold

_logs = []
_ansire = re.compile("\\033\[[^m]+m")


def _strip_ansi(msg):
    return re.sub(_ansire, "", msg)


def add_stderr():
    _logs.append(sys.stderr)


def add_log(logfile):
    _logs.append(open(logfile, "w"))


def close_logs():
    for f in _logs:
        if f is not sys.stderr:
            f.close()


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