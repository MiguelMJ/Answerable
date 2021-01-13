"""Spider Tool for Answerable

This file contains the functions used to wrapp requests following
respecful practices, taking into account robots.txt, conditional
gets, caching contente, etc.
"""

import json
import pathlib
import requests

# from random import random as rnd
from time import sleep

import feedparser
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

from tools.displayer import fg, bold, green, yellow, red
from tools.log import log

_rp = {}  # robots.txt memory
log_who = "Spider"


class _FalseResponse:
    """Object with the required fields to simulate a HTTP response"""

    def __init__(self, code, content):
        self.status_code = code
        self.content = content


def ask_robots(url: str, useragent: str) -> bool:
    """Check if the useragent is allowed to scrap an url

    Parse the robot.txt file, induced from the url, and
    check if the useragent may fetch a specific url.
    """

    url_struct = urlparse(url)
    base = url_struct.netloc
    if base not in _rp:
        _rp[base] = RobotFileParser()
        _rp[base].set_url(url_struct.scheme + "://" + base + "/robots.txt")
        _rp[base].read()
    return _rp[base].can_fetch(useragent, url)


def get(url, cache=True, delay=2):
    """Respectful wrapper around requests.get"""

    useragent = "Answerable v0.1"

    # If a cached answer exists and is acceptable, then return the cached one.
    p = pathlib.Path.cwd() / "data" / "spider" / url.replace("/", "-")
    if cache and p.exists():
        with open(p, "r") as fh:
            res = fh.read().replace("\\r\\n", "")
        log(log_who, "Used cached {}", fg(url, green))
        return _FalseResponse(200, res)

    # If the robots.txt doesn't allow the scraping, return forbidden status
    if not ask_robots(url, useragent):
        log(log_who, fg("robots.txt forbids {}"), fg(url, red))
        return _FalseResponse(403, "robots.txt forbids it")

    # Make the request after the specified delay
    # log("[{}] {}".format(fg("{:4.2f}".format(delay), yellow), url))
    log(log_who, "Waiting to ask for {}", fg(url, yellow))
    log(log_who, "  in {:4.2f} seconds", delay)
    sleep(delay)
    headers = {"User-Agent": useragent}
    log(log_who, "Requesting")
    res = requests.get(url, timeout=10, headers=headers)
    # Exit the program if the scraping was penalized
    if res.status_code == 429:  # too many requests
        log(log_who, bold(red("Too many requests - Aborting")))
        exit()

    # Cache the response if allowed by user
    if cache:
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as fh:
            fh.write(res.content.decode(res.encoding))
        log(log_who, fg("  Cached", green))

    return res


def get_feed(url, store=True):
    """Get RSS feed and optionally remember to reduce bandwith"""

    useragent = "Answerable RSS v0.1"
    log(log_who, "Requesting feed {}", fg(url, yellow))

    # Get the conditions for the GET bandwith reduction
    p = pathlib.Path.cwd() / "data" / "spider" / "feed" / url.replace("/", "-")
    etag = None
    modified = None
    if (p).exists():
        with open(p, "r") as fh:
            headers = json.load(fh)
            etag = headers["etag"]
            modified = headers["modified"]
    log(log_who, "with {}: {}", bold("etag"), fg(etag, yellow))
    log(log_who, "with {}: {}", bold("modified"), (fg(modified, yellow)))

    # Get the feed
    feed = feedparser.parse(url, agent=useragent, etag=etag, modified=modified)

    # Store the etag and/or modified headers if told so
    if store and feed.status != 304:
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w") as fh:
            etag = feed.etag if "etag" in feed else None
            modified = feed.modified if "modified" in feed else None
            json.dump(
                {
                    "etag": etag,
                    "modified": modified,
                },
                fh,
            )
        log(log_who, "Stored new {}: {}", bold("etag"), fg(etag, green))
        log(log_who, "Stored new {}: {}", bold("modified"), fg(modified, green))

    return feed
