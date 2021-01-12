import json
from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel


def recommend(user_qa, feed):

    answered = [
        x[0]["title"] + " " + bs(x[0]["body"], "html.parser").getText(" ", strip=True)
        for x in user_qa
    ]
    tags_ans = [" ".join(x[0]["tags"]) for x in user_qa]

    questions = [x["title"] + x["body"] for x in feed]
    tags_unans = [" ".join(x["tags"]) for x in feed]

    nans = len(answered)
    nunans = len(questions)

    """
    The following code is an adapted version of the Content-Based recommmender
    described in this tutorial:

    https://www.datacamp.com/community/tutorials/recommender-systems-python
    """

    tfidf = TfidfVectorizer(stop_words="english")
    count = CountVectorizer(stop_words="english")

    # list of vectorized body and tags
    tfidf_matrix = tfidf.fit_transform(answered + questions)
    count_matrix = count.fit_transform(tags_ans + tags_unans)

    # similarity matrices: without and with tags
    cosine_sim_body = linear_kernel(tfidf_matrix, tfidf_matrix)
    cosine_sim_tags = linear_kernel(count_matrix, count_matrix) + cosine_sim_body

    # rows: unanswered, cols: answered
    unans_similarity_body = cosine_sim_body[nans:, :nans]
    unans_similarity_tags = cosine_sim_tags[nans:, :nans]

    # form of the following lists: [(feed index, value)]
    sum_sim_body = enumerate([sum(r) for r in unans_similarity_body])
    max_sim_body = enumerate([max(r) for r in unans_similarity_body])
    sum_sim_tags = enumerate([sum(r) for r in unans_similarity_tags])
    max_sim_tags = enumerate([max(r) for r in unans_similarity_tags])

    # sort the indices by the value
    sort_sum_sim_body = sorted(sum_sim_body, key=lambda x: x[1], reverse=True)
    sort_max_sim_body = sorted(max_sim_body, key=lambda x: x[1], reverse=True)
    sort_sum_sim_tags = sorted(sum_sim_tags, key=lambda x: x[1], reverse=True)
    sort_max_sim_tags = sorted(max_sim_tags, key=lambda x: x[1], reverse=True)

    # map each index to its classifications
    by_sum_body = {x[0]: i for i, x in enumerate(sort_sum_sim_body)}
    by_max_body = {x[0]: i for i, x in enumerate(sort_max_sim_body)}
    by_sum_tags = {x[0]: i for i, x in enumerate(sort_sum_sim_tags)}
    by_max_tags = {x[0]: i for i, x in enumerate(sort_max_sim_tags)}

    # compute the mean classification for each index
    mean_index = []
    for i in range(nunans):
        mean = (by_sum_body[i] + by_sum_tags[i] + by_max_body[i] + by_max_tags[i]) / 4
        mean_index.append((mean, i))

    # build the final recommended feed order
    by_mean = [x[1] for x in sorted(mean_index)]

    return by_mean
