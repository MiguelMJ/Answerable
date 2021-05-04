"""Cache Tool for Answerable

This file contains the functions to access and modify cached content.
It may be used by different modules, so each function requires a category argument
to avoid collisions.

As every function is intended to serve a secondary role in extern functions, the
logs have an extra level of indentation.
"""

import json
import pathlib
from datetime import datetime as dt
from datetime import timedelta as td

from tools.log import log
from tools.displayer import fg, green, magenta


__cache_dir = ".cache"


def check(category: str, _file: str, max_delta: td) -> (bool, pathlib.Path):
    """Return if a file is cached and where it is located.

    Returns:
    (B, P) where
    - B is true if the content is cached and usable
    - P is the path where the cached content is/should be.

    Parameters:
    category: Folder inside the cache.
    _file: File name to look for.
    max_delta: Timedelta used as threshold to consider a file too old.
    """

    # Prepare the path to the cached file
    subpath = pathlib.Path(category) / _file
    path = pathlib.Path.cwd() / __cache_dir / subpath
    path.parent.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        log("  Miss {}", fg(subpath, magenta))
        return False, path
    else:
        # Check if the file is too old
        log("  Hit {}", fg(subpath, green))
        modified = dt.fromtimestamp(path.stat().st_mtime)
        now = dt.now()
        delta = now - modified
        log("  Time passed since last fetch: {}", delta)
        valid = delta < max_delta
        if valid:
            log(fg("  Recent enough", green))
        else:
            log(fg("  Too old", magenta))
        return valid, path


def update(category: str, _file: str, obj, json_format=True):
    """Update or create a file in the cache

    Parameters:
    category: Folder inside the cache.
    _file: File name to store in.
    obj: Serializable object to store.
    """

    subpath = pathlib.Path(category) / _file
    path = pathlib.Path.cwd() / __cache_dir / subpath
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as fh:
        if json_format:
            json.dump(obj, fh, indent=2)
        else:
            fh.write(obj)
    log("  Cache updated: {}", fg(subpath, green))
