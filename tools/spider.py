import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from random import random as rnd
from time import sleep

import pathlib

rp = {}

class FalseResponse:
    def __init__(self,code,content):
        self.status_code = code
        self.content = content

def get(url, cache=True):
    # Check the cache
    p = pathlib.Path.cwd() / 'data' / 'spider' / pathlib.Path(url)
    if(cache and p.exists()):
        with open(p,'r') as fh:
            res = fh.read().replace("\\r\\n",'')
        print('[\033[38;2;0;250;0mCACHE\033[0m]',url)
        return FalseResponse(200,res)
    
    p.parent.mkdir(parents=True, exist_ok=True)
    # Check the robot.txt
    url_struct = urlparse(url)
    base = url_struct.netloc
    if base not in rp:
        rp[base] = RobotFileParser()
        rp[base].set_url(url_struct.scheme+'://'+base+'/robots.txt')
        rp[base].read()
    if not rp[base].can_fetch("*",url):
        return FalseResponse(403,'robots.txt forbids it')
    # Or make the petition
    t = rnd()*5+2
    print('[\033[38;2;250;250;0m{:4.2f}\033[0m] {}'.format(t, url))
    sleep(t)
    res = requests.get(url,timeout=10)
    with open(p,'w') as fh:
        fh.write(str(res.content))
        print('\tCached')
    if(res.status_code == 429): # too many requests
        print('TOO MANY REQUESTS: ABORTING')
        exit()
    return res


