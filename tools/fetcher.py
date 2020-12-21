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
        print("Time since last crawl:", delta)
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
        user_qa[0]["tags"] = user_qa[1].pop("tags")
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


"""
def get_all_question_feed():
    return get_question_feed('https://stackoverflow.com/feeds')

def get_tagged_question_feed(tag_info):
    return sum([get_question_feed('https://stackoverflow.com/feeds/tag/'+tag) for tag in tag_info],[])
"""

"""
def get_answers(user_id):
    cache_file = 'user_'+user_id+'.json' 
    cached, fp = check_cache(cache_file)
    if(cached):
        with open(fp, 'r') as cache:
            ans_list = json.load(cache)
        return [Answer.fromMap(obj) for obj in ans_list]
    else:
        ans_list = [get_answer(sumry) for sumry in get_summaries(user_id)]
        with open(fp, 'w') as cache:
            cache.write('['+','.join(a.toJSON() for a in ans_list)+']')
        return ans_list
    
def get_summaries(user_id):
    url_format = 'https://stackoverflow.com/users/{}?tab=answers&page={}'
    page=1
    results=[]
    while(True):
        # Get page
        print('Inspecting page',page)
        url_struct = urlparse(url_format.format(user_id,page))
        url = url_struct.geturl()
        result = spider.get(url, cache=False)
        while(result.status_code == 301): # Follow permanently moved links
            url = url_struct.scheme+'://'+url_struct.netloc+'/'+result.headers['location']
            result = spider.get(url)
            
        if(result.status_code != 200):
            print(result)
            return results
        # Parse summaries of answers
        soup = BeautifulSoup(result.content, 'html.parser')
        
        summaries = soup.find_all('div',class_='answer-summary')
        for post in summaries:
            votes = post.find(class_='answer-votes')
            accepted = 'answered-accepted' in votes.attrs['class']
            votes = int(votes.getText('',strip=True))
            link = post.find(class_='answer-hyperlink')
            href = link['href']
            title = str(link.getText('',strip=True))
            results.append(Summary(title,votes,accepted,href))
        if(len(summaries) == 0):
            break
        page += 1
    return results

def get_answer(summary):
    url = 'https://stackoverflow.com'+summary.link
    answer_id = 'answer-{}'.format(summary.identifier)
    
    result = spider.get(url)
    if(result.status_code != 200):
        print(result)
        return None
    soup = BeautifulSoup(result.content, 'html.parser')
    
    question = soup.find(id='question')
    qBody = question.find(attrs={'itemprop':'text'}).getText(' ',strip=True)
    aBody = soup.find(id=answer_id).find(attrs={'itemprop':'text'}).getText(' ',strip=True)
    tags = [x.getText('',strip=True) for x in question.find_all('a',class_='post-tag')]
    
    return Answer(summary, qBody, aBody, tags)
"""
