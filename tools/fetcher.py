"""Fetcher Tool for Answerable

This file contains the high level functions in charge of data retrieval.
It provides a interface between the spider/crawler and another level of
cacheable information.
"""

import json
from datetime import timedelta as td

from bs4 import BeautifulSoup

from tools import spider, cache
from tools.log import log, abort
from tools.displayer import fg, magenta, green, bold

log_who = "Fetcher"
cache_where = "fetcher"
cache_threshold = td(hours=12)


def get_QA(user_id, force_reload=False):
    """Retrieve information about the questions answered by the user

    Returns a structure with the following format:
      [
        [Question_1, Answer_1],
        [Question_2, Answer_2],
        ...
      ]

    where Question_n has the following keys:
      view_count: int
      score: int
      creation_date: timestamp
      question_id: int
      link: str
      title: str
      body: str (html)
      tags: list of str

    and Answer_n has the following keys:
      is_accepted: bool
      score: int
      question_id: int
      link: str
      title: str
      body: str (html)
    """

    log(log_who, bold("Fetching user information"))
    cache_file = str(user_id) + ".json"
    # Check cache
    if not force_reload:
        hit, fpath = cache.check(cache_where, cache_file, cache_threshold)
        if hit:
            with open(fpath) as fh:
                stored = json.load(fh)
            return stored
    # Get the answers
    api_request_f = "https://api.stackexchange.com/2.2/users/{}/answers?page={}&order=desc&sort=creation&site=stackoverflow&filter=!.Fjr43gf6UvsWf.-.z(SMRV3sqodT"
    page = 1
    answers = []
    while True:
        api_request = api_request_f.format(user_id, page)
        response = spider.get(api_request)
        if response.status_code != 200:
            abort(log_who, response)
        result = json.loads(response.content)
        answers += result["items"]
        if not result["has_more"]:
            break
        page += 1
    # Get the questions
    api_request_f = "https://api.stackexchange.com/2.2/questions/{}?page={}&order=desc&sort=creation&site=stackoverflow&filter=!5RCLVFC_3nVp6Kjoti6BKirZj"
    questions = []
    max_ids = 100  # no more than 100 ids allowed at once
    k = int(len(answers) / max_ids) + 1
    for i in range(0, k):
        subset = answers[i * max_ids : (i + 1) * max_ids]
        q_ids = ";".join([str(a["question_id"]) for a in subset])
        page = 1
        while True:
            api_request = api_request_f.format(q_ids, page)
            response = spider.get(api_request, False)  # urls too long to cache
            if response.status_code != 200:
                abort(log_who, response)
            result = json.loads(response.content)
            questions += result["items"]
            if not result["has_more"]:
                break
            page += 1
    # Join answers and questions
    user_qa = [
        [q, a]
        for q in questions
        for a in answers
        if q["question_id"] == a["question_id"]
    ]
    for qa in user_qa:
        qa[0]["tags"] = qa[1].pop("tags")

    cache.update(cache_where, cache_file, user_qa)

    return user_qa


def get_question_feed(url):
    """Retrieve the last questions of the feed

    Returns a structure with the followint format:
      [Question_1, Question_2, ...]

    where Question_n has the following keys:
      link: str
      title: str
      body: str (html)
      tags: list of str
    """

    log(log_who, bold("Fetching question feed"))
    feed = spider.get_feed(url)
    if feed.status == 304:  # Not Modified
        log(log_who, fg("Feed not modified since last retrieval (status 304)", magenta))
        return []
    log(log_who, "Number of entries in feed: {}", fg(len(feed.entries), green))
    questions = []
    for entry in feed.entries:
        soup = BeautifulSoup(entry.summary, "html.parser")
        q = {
            "link": entry.link,
            "title": entry.title,
            "body": soup.getText(" ", strip=True),
            "tags": [x["term"] for x in entry.tags],
        }
        questions.append(q)
    return questions


def get_user_tags(filename):
    """Parse the tags file and return the user followed and ignored tags"""

    try:
        with open(filename, "r") as fh:
            bs = BeautifulSoup(fh.read(), "html.parser")
        return {
            "followed": [
                x.getText(" ", strip=True)
                for x in bs.find(id="watching-1").find_all("a", class_="post-tag")
            ],
            "ignored": [
                x.getText(" ", strip=True)
                for x in bs.find(id="ignored-1").find_all("a", class_="post-tag")
            ],
        }
    except FileNotFoundError:
        abort(log_who, "File not found: {}", filename)
