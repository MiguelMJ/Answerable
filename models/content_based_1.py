"""Recommender Tool for Answerable

This file contains the recommendation algorithm.
"""

from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np
import re


def preprocessed_text_from_html(html):
    soup = bs(html, "html.parser")
    for tag in soup.findAll(name="code"):
        tag.decompose()
    text = soup.getText(" ", strip=True)
    text = re.sub(r"\d+", "", text)
    text = " ".join(re.findall(r"[\w+_]+", text))
    return text.lower()


def recommend(user_qa, feed):

    answered = [
        " ".join(x["tags"])
        + " "
        + x["title"].lower()
        + " "
        + preprocessed_text_from_html(x["body"])
        for [x, _] in user_qa
    ]

    unanswered = [
        " ".join(x["tags"])
        + " "
        + x["title"].lower()
        + " "
        + preprocessed_text_from_html(x["body"])
        for x in feed
    ]

    nans = len(answered)

    tfidf = TfidfVectorizer(stop_words="english")

    # list of vectorized text
    tfidf_matrix = tfidf.fit_transform(answered + unanswered)

    # similarity matrix of each answer with the rest
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # rows: unanswered, cols: answered
    unans_similarity = cosine_sim[nans:, :nans]

    # index: unanswered. values: max similarity and score
    max_sim = list(enumerate([max(r) for r in unans_similarity]))
    score = [x * len(unanswered[i].split()) for i,x in max_sim]
    
    # sort the indices by the value
    by_score = sorted(list(enumerate(score)), key=lambda x: x[1], reverse=True)
    
    # relation between index in feed and index of closest answered
    closest = [
        (i, np.where(np.isclose(unans_similarity[i], v))[0][0]) 
        for i, v in max_sim
    ]
    info = []
    for unans, ans in closest:
        info.append(
            "{} of similarity with {}. Score: {}".format(
                f"{100*max_sim[unans]:.2f}%",
                user_qa[ans][0]["title"],
                f"{100*score[unans]:.2f}"
            )
        )

    # get the indexes, now sorted
    by_max = [x[0] for x in by_score]

    return by_max, info
