import pathlib
import json
from datetime import datetime as dt
from datetime import timedelta as td

from urllib.parse import urlparse
from bs4 import BeautifulSoup

from tools import spider
from models.summary import Summary
from models.answer import Answer

def check_cache(filename):
    cache_dir = 'data'
    threshold = td(days=1)
    cache_path = pathlib.Path.cwd() / cache_dir
    cache_path.mkdir(parents=True,exist_ok=True)
    filepath = cache_path / filename
    if(not filepath.exists()):
        return False, filepath
    else:
        modified = dt.fromtimestamp(filepath.stat().st_mtime)
        now = dt.now()
        delta = now - modified
        print('Time since last crawl:', delta)
        return delta < threshold, filepath
    
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
    
    
