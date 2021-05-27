"""Recommender Tool for Answerable

This file contains the recommendation algorithm.
"""
import tools.displayer

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

    # index: unanswered. values: max similarity, text size and score
    max_sim = list(enumerate([max(r) for r in unans_similarity]))
    unans_sizes = [len(u.split()) for u in unanswered]
    score = [x * x * unans_sizes[i] for i, x in max_sim]

    # sort the indices by the value
    by_score = sorted(list(enumerate(score)), key=lambda x: x[1], reverse=True)

    # relation between index in feed and index of closest answered
    closest = [
        (i, np.where(np.isclose(unans_similarity[i], v))[0][0]) for i, v in max_sim
    ]

    # store displayable information
    b = tools.displayer.bold
    info_f = "{}: {{}}\n{}:{{}} {}: {{}} {}: {{}}".format(
        b("Closest"),
        b("Text size"),
        b("Similarity"),
        b("Score"),
    )
    info = []
    for unans, ans in closest:
        info.append(
            info_f.format(
                user_qa[ans][0]["title"],
                unans_sizes[unans],
                f"{100*max_sim[unans][1]:.2f}%",
                f"{score[unans]:.2f}",
            )
        )

    # get the indexes, now sorted
    sorted_index = [x[0] for x in by_score]

    return sorted_index, info
