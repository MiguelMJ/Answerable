import re
import json

from tools.spider import get
from tools import log

def latest():
    try:
        res = get("https://api.github.com/repos/MiguelMJ/Answerable/releases/latest", 0)
        if(res.status_code != 200):
            log.warn("Unable to get information from latest version")
            return None
        latest = re.search(r'v[\d.]+.?', json.loads(res.content)['name'])[0]
        return latest
    except URLError:
        log.warn("Unable to get information from latest version")
    return None
        
