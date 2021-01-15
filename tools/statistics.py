"""Statistics Tool for Answerable

This file contains the functions used to analyze user answers.
"""

#
# TAG RELATED METRICS (USING QA)
#
_tags_info = None


def tags_info(qa):
    """Map each tag to its score, acceptance and count"""

    global _tags_info
    if _tags_info is not None:
        return _tags_info
    tags_info = {}
    for x in qa:
        for t in x[0]["tags"]:
            tc = tags_info.get(t, (0, 0, 0))  # (score, acceptance, count)
            tc = (tc[0] + x[1]["score"], tc[1] + x[1]["is_accepted"], tc[2] + 1)
            tags_info[t] = tc
    _tags_info = tags_info
    return tags_info


def top_tags_use(qa, top=5):
    """Top tags by appearance"""

    tags = tags_info(qa)
    sorted_tags = sorted(tags, key=lambda x: tags[x][2], reverse=True)
    return [(x, tags[x][2]) for x in sorted_tags][:top]


def top_tags_score_abs(qa, top=5):
    """Top tags by accumulated score"""

    tags = tags_info(qa)
    sorted_tags = sorted(tags, key=lambda x: tags[x][0], reverse=True)
    return [(x, tags[x][0]) for x in sorted_tags][:top]


def top_tags_acceptance_abs(qa, top=5):
    """Top tags by accumulated acceptance"""

    tags = tags_info(qa)
    sorted_tags = sorted(
        tags,
        key=lambda x: tags[x][1],
        reverse=True,
    )
    return [(x, tags[x][1]) for x in sorted_tags][:top]


def top_tags_score_rel(qa, top=5):
    """Top tags by score per answer"""

    tags = tags_info(qa)
    sorted_tags = sorted(tags, key=lambda x: tags[x][0] / tags[x][2], reverse=True)
    return [(x, tags[x][0] / tags[x][2]) for x in sorted_tags][:top]


def top_tags_acceptance_rel(qa, top=5):
    """Top tags by acceptance per answer"""

    tags = tags_info(qa)
    sorted_tags = sorted(tags, key=lambda x: tags[x][1] / tags[x][2], reverse=True)
    return [(x, tags[x][1] / tags[x][2]) for x in sorted_tags][:top]


#
# ANSWER RELATED METRICS
#
def top_answers(answers, top=5):
    """Top answers by score"""

    return sorted(answers, key=lambda x: x["score"], reverse=True)[:top]


def top_accepted(answers, top=5):
    """Top accepted answers by score"""

    return list(
        filter(
            lambda x: x["is_accepted"],
            sorted(answers, key=lambda x: x["score"], reverse=True),
        )
    )[:top]


#
# REPUTATION RELATED METRICS
#
def reputation(answer):
    """Reputation associated to an answers"""

    return answer["score"] * 10 + answer["is_accepted"] * 15


_answers_sorted_reputation = None
_total_reputation = None


def answers_sorted_reputation(answers):
    """Answers sorted by associated reputation"""

    global _answers_sorted_reputation
    if _answers_sorted_reputation is None:
        _answers_sorted_reputation = sorted(
            answers, key=lambda x: reputation(x), reverse=True
        )
    return _answers_sorted_reputation


def total_reputation(answers):
    """Total reputation gained from answers"""

    global _total_reputation
    if _total_reputation is None:
        _total_reputation = sum([reputation(a) for a in answers])
    return _total_reputation


def average_reputation_weight(answers, w):
    """Average reputation and weight of answers generating w % reputation"""

    repw = total_reputation(answers) * w
    sorted_answers = answers_sorted_reputation(answers)
    acc_rep = 0
    acc_ans = 0
    while acc_rep < repw and acc_ans < len(sorted_answers):
        acc_rep += reputation(sorted_answers[acc_ans])
        acc_ans += 1
    return (acc_rep / acc_ans, 100 * acc_ans / len(answers))


#
# LISTS TO SIMPLIFY CALLING
#
tag_metrics = [  # call with qa
    ("Top used tags", top_tags_use),
    ("Top tags by accumulated score", top_tags_score_abs),
    ("Top tags by score per answer", top_tags_score_rel),
    ("Top tags by accumulated acceptance", top_tags_acceptance_abs),
    ("Top tags by acceptance per answer", top_tags_acceptance_rel),
]
answer_metrics_single = [  # call with answers
    ("Answers analyzed", len),
    ("Total score", lambda x: sum([a["score"] for a in x])),
    ("Average score", lambda x: sum([a["score"] for a in x]) / len(x)),
    ("Total accepted", lambda x: sum([a["is_accepted"] for a in x])),
    ("Acceptance ratio", lambda x: sum([a["is_accepted"] for a in x]) / len(x)),
]
answer_metrics_tops = [  # call with answers
    ("Top answers by score", top_answers, lambda a: a["score"]),
    ("Top accepted answers by score", top_accepted, lambda a: a["score"]),
]
reputation_metrics_single = [  # call with answers
    ("Total reputation", lambda x: sum([reputation(a) for a in x])),
    ("Average reputation", lambda x: sum([reputation(a) for a in x]) / len(x)),
]
reputation_weight_metrics = (  # call with answers and weights
    [0.95, 0.80],
    average_reputation_weight,
    (
        "Average reputation on answers generating {:.0f}% reputation",
        "Percentage of answers generating {:.0f}% reputation",
    ),
)
