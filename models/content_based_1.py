"""Recommender Tool for Answerable

This file contains the recommendation algorithm.
"""

from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
import nltk
import numpy as np
import re
from collections import Counter


def preprocessed_text_from_html(html):
    soup = bs(html, "html.parser")
    for tag in soup.findAll(name="code"):
        tag.decompose()
    text = soup.getText(" ", strip=True)
    text = re.sub(r"\d+", "", text)
    text = " ".join(re.findall(r"[\w+_]+", text))
    return text.lower()


def counts(text):
    counter = Counter(text.split())
    return sorted([(counter[x], x) for x in counter], reverse=True)


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
    nunans = len(unanswered)

    """
    The following code is an adapted version of the Content-Based recommmender
    described in this tutorial:

    https://www.datacamp.com/community/tutorials/recommender-systems-python
    """

    tfidf = TfidfVectorizer(stop_words="english")

    # list of vectorized body and tags
    tfidf_matrix = tfidf.fit_transform(answered + unanswered)

    # similarity matrices: without and with tags
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # rows: unanswered, cols: answered
    unans_similarity = cosine_sim[nans:, :nans]

    # form of the following list: [(feed index, value)], where value is the
    # value of the maximum similarity with a single answered question
    max_sim = list(enumerate([max(r) for r in unans_similarity]))

    # sort the indices by the value
    sort_max_sim = sorted(max_sim, key=lambda x: x[1], reverse=True)

    closest = [
        (i, np.where(np.isclose(unans_similarity[i], v))[0][0]) for i, v in sort_max_sim
    ]
    info = []
    stw = set(nltk.corpus.stopwords.words("english"))
    for u, a in closest:
        info.append(
            "Closest: {} ({})".format(
                user_qa[a][0]["title"], f"{100*max_sim[u][1]:.2f}%"
            )
        )

    # get the indexes, now sorted
    by_max = [x[0] for x in sort_max_sim]

    return by_max, info
