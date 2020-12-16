import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
import feedparser

import pathlib
import json
from random import random as rnd
from time import sleep

from tools.displayer import fg, green, yellow

rp = {}

class FalseResponse:
    def __init__(self,code,content):
        self.status_code = code
        self.content = content

def get(url, cache=True):
    useragent = 'Answerable v0.1'
    # Check the cache
    p = pathlib.Path.cwd() / 'data' / 'spider' / url.replace('/','-')
    if(cache and p.exists()):
        with open(p,'r') as fh:
            res = fh.read().replace("\\r\\n",'')
        print(fg('CACHE',green),url)
        return FalseResponse(200,res)
    
    p.parent.mkdir(parents=True, exist_ok=True)
    # Check the robot.txt
    url_struct = urlparse(url)
    base = url_struct.netloc
    if base not in rp:
        rp[base] = RobotFileParser()
        rp[base].set_url(url_struct.scheme+'://'+base+'/robots.txt')
        rp[base].read()
    if not rp[base].can_fetch(useragent,url):
        return FalseResponse(403,'robots.txt forbids it')
    # Or make the petition
    # t = rnd()*5+2
    t = 2
    print('[{}] {}'.format(fg('{:4.2f}'.format(t),yellow), url))
    sleep(t)
    headers = {
        'User-Agent':useragent
    }
    res = requests.get(url,timeout=10, headers=headers)
    if cache:
        with open(p,'w') as fh:
            fh.write(res.content.decode(res.encoding))
            print('\tCached')
    if(res.status_code == 429): # too many requests
        print('TOO MANY REQUESTS: ABORTING')
        exit()
    return res

def get_feed(url, store=True):
    useragent = 'Answerable RSS v0.1'
    p = pathlib.Path.cwd() / 'data' / 'feed' / url.replace('/','-')
    etag = None
    modified = None
    if((p).exists()):
        with open(p,'r') as fh:
            headers = json.load(fh)
            etag = headers['etag']
            modified = headers['modified']
    feed = feedparser.parse(url, agent=useragent, etag=etag, modified=modified)
    if(store):
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p,'w') as fh:
            json.dump({'etag':feed.etag if 'etag' in feed else None,
                       'modified':feed.modified if 'modified' in feed else None}, 
                    fh)
    return feed
