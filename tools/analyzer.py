import re

from models.tag import Tag
from models.word import Word


def word_list(text):
    ignored = {"the", "and", "but", "its", "than", "was", "their"}
    wlist = re.findall(r"\b[a-z]{3,30}\b", text.lower())
    wlist = [w for w in wlist if w not in ignored]
    return wlist


def tag_info(user_qa, normalize=True):
    tags = dict()
    total_rep = 0
    for qa in user_qa:
        for t in qa[0]["tags"]:
            info = tags.get(t, Tag(t))
            info.count += 1
            rep = qa[1]["score"] * 10 + (qa[1]["is_accepted"] and 15 or 0)
            info.reputation += rep
            total_rep += rep
            tags[t] = info
    if normalize:
        for k in tags:
            tags[k].reputation /= total_rep
    return tags


def word_info(questions, normalize=True):
    words = dict()
    total_f = 0
    for q in questions:
        wlist = word_list(q["body"])
        for w in wlist:
            word = words.get(w, Word(w, 0, set()))
            word.tags |= set(q["tags"])
            word.frequency += 1
            words[w] = word
            total_f += 1
    if normalize:
        for k in words:
            words[k].frequency /= total_f
    return words


def word_expected_reputation(w, word_info, tag_info):
    word = word_info.get(w, Word(w, 1, set()))
    w_freq = word.frequency
    w_tag_factor = sum(tag_info[x].ratio() for x in word.tags)
    w_factor = w_freq * w_tag_factor
    return w_factor


def question_expected_reputation(question, word_info, tag_info):
    wlist = word_list(question["body"])
    rep = sum(tag_info[x].ratio() for x in question["tags"] if x in tag_info)
    for w in wlist:
        rep += word_expected_reputation(w, word_info, tag_info)
    return rep
