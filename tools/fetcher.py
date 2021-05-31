"""Fetcher Tool for Answerable

This file contains the high level functions in charge of data retrieval.
It provides a interface between the spider/crawler and another level of
cacheable information.
"""

import math
import json
from datetime import timedelta as td

from bs4 import BeautifulSoup

from tools import spider, cache
from tools.log import log, abort
from tools.displayer import fg, magenta, green, bold

cache_where = "fetcher"
cache_threshold = td(hours=12)


def get_questions(question_ids):
    """Retrieve questions from Stack Overflow

    - question_ids: list of question IDs

    Returns a list of objects with the following attributes:
      {
        "tags": [string],
        "answers": [ {"owner": {"user_id": int}} ],
        "score": int,
        "creation_date": timestamp,
        "question_id": int,
        "link": string,
        "title": string,
        "body": string (html)
      }
    """
    # about this request: https://api.stackexchange.com/docs/questions-by-ids#page=1&pagesize=100&order=desc&sort=creation&ids=67519195&filter=!)So8N7tfWBeyaWUex((*Ndu7tpA&site=stackoverflow
    api_request_f = "https://api.stackexchange.com//2.2/questions/{}?page={}&pagesize=100&order=desc&sort=creation&site=stackoverflow&filter=!)So8N7tfWBeyaWUex((*Ndu7tpA"
    max_ids = 100  # no more than 100 ids allowed at once
    k = math.ceil(len(question_ids) / max_ids)
    log(f"{len(question_ids)} questions, {k} batches")
    questions = []
    for i in range(k):
        log(f"batch {i+1}")
        batch_begin = i * max_ids
        batch_end = i * max_ids + max_ids
        subset = ";".join(question_ids[batch_begin:batch_end])
        page = 1
        while True:
            api_request = api_request_f.format(subset, page)
            response = spider.get(
                api_request, delay=0.5, use_cache=False
            )  # urls too long to cache
            if response.status_code != 200:
                abort(response)
            result = json.loads(response.content)
            questions += result["items"]
            if not result["has_more"]:
                break
            page += 1
    return questions


def get_user_answers(user_id, force_reload=False, max_page=math.inf):
    """Retrieve answers from a Stack Overflow user

    - user_id: user ID

    Returns a list of objects with the following attributes:
      {
        "is_accepted": bool,
        "score": int,
        "questions_id": int,
        "link": string,
        "title": string,
        "body": string (html),
      }
    """

    api_request_f = "https://api.stackexchange.com/2.2/users/{}/answers?page={}&pagesize=100&order=desc&sort=activity&site=stackoverflow&filter=!37n)Y*a2Ut6eDilfH4XoIior(X(b8nm7Z-g)Tgl*A4Qdfe8Mcn-Luu"
    page = 1
    answers = []
    while page <= max_page:
        api_request = api_request_f.format(user_id, page)
        response = spider.get(
            api_request, delay=0.5, max_delta=td() if force_reload else td(hours=12)
        )
        if response.status_code != 200:
            abort(response)
        result = json.loads(response.content)
        answers += result["items"]
        if not result["has_more"]:
            break
        page += 1
    return answers


def get_QA(user_id, force_reload=False, max_page=5):
    """Retrieve information about the questions answered by the user

    Return
        [
            (Question_1, Answer_1),
            (Question_2, Answer_2),
            ...
        ]
    See
        get_questions, get_user_answers
    """

    log(bold("Fetching user information"))
    if force_reload:
        log(fg("Force reload", magenta))
    cache_file = str(user_id) + ".json"
    # Check cache
    if not force_reload:
        hit, fpath = cache.check(cache_where, cache_file, cache_threshold)
        if hit:
            with open(fpath) as fh:
                stored = json.load(fh)
            return stored
    # Get the answers
    answers = get_user_answers(user_id, force_reload, max_page)

    # Get the questions
    q_ids = [str(a["question_id"]) for a in answers]
    questions = get_questions(q_ids)

    # Join answers and questions
    user_qa = [
        (q, a)
        for q in questions
        for a in answers
        if q["question_id"] == a["question_id"]
    ]
    cache.update(cache_where, cache_file, user_qa)
    for q, a in user_qa:
        a["tags"] = q["tags"]

    ## Include questions specified by user
    try:
        with open(".additional_training", "r") as f:
            extra_q_ids = f.read().split()
        log("Aditional training: " + str(extra_q_ids))
        extra_questions = get_questions(extra_q_ids)
    except FileNotFoundError:
        extra_questions = []
        log("No additional training specified by user")
    user_qa += [(q, None) for q in extra_questions]

    return user_qa


def get_question_feed(url, force_reload=False):
    """Retrieve the last questions of the feed

    Returns a structure with the following format:
      [Question_1, Question_2, ...]

    where Question_n has the following keys:
      link: str
      title: str
      body: str (html)
      tags: list of str
    """

    log(bold("Fetching question feed"))
    if force_reload:
        log(fg("Force reload", magenta))
    feed = spider.get_feed(url, force_reload=force_reload)
    if feed.status == 304:  # Not Modified
        log(fg("Feed not modified since last retrieval (status 304)", magenta))
        return []
    log("Number of entries in feed: {}", fg(len(feed.entries), green))
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
        abort("File not found: {}", filename)
