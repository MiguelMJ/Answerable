import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from models.summary import Summary

def get_summaries(user_id):
    url_format = 'https://stackoverflow.com/users/{}?tab=answers&sort=votes&page={}'
    page=1
    results=[]
    while(True):
        # Get page
        print('Inspecting page',page, end='')
        url_struct = urlparse(url_format.format(user_id,page))
        url = url_struct.geturl()
        result = requests.get(url)
        while(result.status_code == 301): # Follow permanently moved links
            url_struct['path'] = result.headers['location']
            url = url_struct.geturl()
            result = requests.get(url)
            
        if(result.status_code != 200):
            print(result)
            return results
        print('\r',end='')
        # Parse summaries of answers
        soup = BeautifulSoup(result.content, 'html.parser')
        
        summaries = soup.find_all("div",class_="answer-summary")
        for post in summaries:
            votes = post.find(class_='answer-votes')
            accepted = 'answered-accepted' in votes.attrs['class']
            votes = int(votes.getText('',strip=True))
            link = post.find(class_='answer-hyperlink')
            href = link['href']
            title = str(link.getText('',strip=True))
            results.append(Summary(title,votes,accepted,link))
        if(len(summaries) == 0):
            break
        page += 1
    return results

def get_answer(summary):
    url = "https://stackoverflow.com"+summary.link
    result = requests.get(url)
    if(result.status_code != 200):
        print(result)
        return None
    soup = BeautifulSoup(result.content, 'html.parser')
    
        
