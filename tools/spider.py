"""Spider Tool for Answerable

This file contains the functions used to wrapp requests following
respecful practices, taking into account robots.txt, conditional
gets, caching contente, etc.
"""

import json
import requests

# from random import random as rnd
from time import sleep
from datetime import timedelta as td

import feedparser
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

from tools import cache
from tools.displayer import fg, bold, green, yellow, red
from tools.log import log, abort

_rp = {}  # robots.txt memory


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


def get(url, delay=2, use_cache=True, max_delta=td(hours=12)):
    """Respectful wrapper around requests.get"""

    useragent = "Answerable v0.1"

    # If a cached answer exists and is acceptable, then return the cached one.

    cache_file = url.replace("/", "-")
    if use_cache:
        log("Checking cache before petition {}", fg(url, yellow))
        hit, path = cache.check("spider", cache_file, max_delta)
        if hit:
            with open(path, "r") as fh:
                res = fh.read().replace("\\r\\n", "")
            return _FalseResponse(200, res)

    # If the robots.txt doesn't allow the scraping, return forbidden status
    if not ask_robots(url, useragent):
        log(fg("robots.txt forbids {}", red), url)
        return _FalseResponse(403, "robots.txt forbids it")

    # Make the request after the specified delay
    # log("[{}] {}".format(fg("{:4.2f}".format(delay), yellow), url))
    log("Waiting to ask for {}", fg(url, yellow))
    log("  in {:4.2f} seconds", delay)
    sleep(delay)
    headers = {"User-Agent": useragent}
    log("Requesting")
    res = requests.get(url, timeout=10, headers=headers)
    # Exit the program if the scraping was penalized
    if res.status_code == 429:  # too many requests
        abort("Too many requests")

    # Cache the response if allowed by user
    if use_cache:
        cache.update(
            "spider", cache_file, res.content.decode(res.encoding), json_format=False
        )

    return res


def get_feed(url, force_reload=False):
    """Get RSS feed and optionally remember to reduce bandwith"""

    useragent = "Answerable RSS v0.1"
    log("Requesting feed {}", fg(url, yellow))
    cache_file = url.replace("/", "_")

    # Get the conditions for the GET bandwith reduction
    etag = None
    modified = None
    if not force_reload:
        hit, path = cache.check("spider.rss", cache_file, td(days=999))
        if hit:
            with open(path, "r") as fh:
                headers = json.load(fh)
                etag = headers["etag"]
                modified = headers["modified"]
        log("with {}: {}", bold("etag"), fg(etag, yellow))
        log("with {}: {}", bold("modified"), fg(modified, yellow))

    # Get the feed
    feed = feedparser.parse(url, agent=useragent, etag=etag, modified=modified)

    # Store the etag and/or modified headers
    if feed.status != 304:
        etag = feed.etag if "etag" in feed else None
        modified = feed.modified if "modified" in feed else None
        new_headers = {
            "etag": etag,
            "modified": modified,
        }
        cache.update("spider.rss", cache_file, new_headers)
        log("Stored new {}: {}", bold("etag"), fg(etag, green))
        log("Stored new {}: {}", bold("modified"), fg(modified, green))

    return feed
