import re

from models.tag import Tag
from models.word import Word

def word_list(text):
    ignored = {
        'the',
        'and',
        'but',
        'its',
        'than',
        'was',
        'their'
    }
    wlist = re.findall(r'\b[a-z]{3,30}\b', text.lower())
    wlist = [w for w in wlist if w not in ignored]
    return wlist

def tag_info(answers, normalize=True):
    tags = dict()
    total_rep=0
    for ans in answers:
        for t in ans.tags:
            info = tags.get(t,Tag(t))
            info.count += 1
            info.reputation += ans.summary.reputation
            total_rep += ans.summary.reputation
            tags[t] = info
    if normalize:
        for k in tags:
            tags[k].reputation /= total_rep
    return list(tags.values())

def word_info(answers, normalize=True):
    words = dict()
    total_f = 0
    for ans in answers:
        wlist = word_list(ans.qBody)
        for w in wlist:
            word = words.get(w,Word(w,0,set()))
            word.tags |= set(ans.tags)
            word.frequency += 1
            words[w] = word
            total_f += 1
    if normalize:
        for k in words:
            words[k].frequency /= total_f
    return list(words.values())

def expected_reputation(answer, word_info, tag_info):
    word_dict = {x.word:x for x in word_info}
    tag_dict = {x.name:x for x in tag_info}
    wlist = word_list(answer.qBody)
    ans_factor = sum(tag_dict[x].ratio() for x in answer.tags if x in tag_dict)
    for w in wlist:
        word = word_dict.get(w,Word(w,1,set()))
        w_freq = word.frequency
        w_tag_factor = sum(tag_dict[x].ratio() for x in word.tags)
        w_factor = w_freq * w_tag_factor
        ans_factor += w_factor
    return ans_factor
