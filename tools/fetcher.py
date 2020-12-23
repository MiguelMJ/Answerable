import json
import pathlib
from datetime import datetime as dt
from datetime import timedelta as td

from bs4 import BeautifulSoup

from tools import spider

__cache_dir = "data"
__threshold = td(days=1)


def check_cache(filename):
    cache_path = pathlib.Path.cwd() / __cache_dir
    cache_path.mkdir(parents=True, exist_ok=True)
    filepath = cache_path / filename
    if not filepath.exists():
        return False, filepath
    else:
        modified = dt.fromtimestamp(filepath.stat().st_mtime)
        now = dt.now()
        delta = now - modified
        # print("Time since last crawl:", delta)
        return delta < __threshold, filepath


def update_cache(filename, obj):
    cache_path = pathlib.Path.cwd() / __cache_dir
    cache_path.mkdir(parents=True, exist_ok=True)
    filepath = cache_path / filename
    with open(filepath, "w") as fh:
        json.dump(obj, fh, indent=2)


def get_QA(user_id):
    cache_file = str(user_id) + ".json"
    # Check cache
    hit, fpath = check_cache(cache_file)
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
            print(response)
            exit()
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
        q_ids = ";".join([str(a["question_id"]) for a in answers])
        page = 1
        while True:
            api_request = api_request_f.format(q_ids, page)
            response = spider.get(api_request, False)  # urls too long to cache
            if response.status_code != 200:
                print(response)
                exit()
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
    update_cache(cache_file, user_qa)
    return user_qa


def get_question_feed(url):
    feed = spider.get_feed(url, False)
    if feed.status == 304:  # Not Modified
        return []
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
