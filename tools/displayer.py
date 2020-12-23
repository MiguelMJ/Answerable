from tools.analyzer import word_expected_reputation

red = (250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)

cyan = (0, 250, 250)
magenta = (250, 0, 250)
yellow = (250, 250, 0)

white = (250, 250, 250)
gray1 = (200, 200, 200)
gray2 = (150, 150, 150)
gray3 = (100, 100, 100)
gray4 = (50, 50, 50)
black = (0, 0, 0)

ansi = True


def lighten(c, r):
    dr = (250 - c[0]) * r
    dg = (250 - c[1]) * r
    db = (250 - c[2]) * r
    return (int(c[0] + dr), int(c[1] + dg), int(c[2] + db))


def darken(c, r):
    dr = c[0] * r
    dg = c[1] * r
    db = c[2] * r
    return (int(c[0] - dr), int(c[1] - dg), int(c[2] - db))


def interpolate(c, d, r):
    dr = (d[0] - c[0]) * r
    dg = (d[1] - c[1]) * r
    db = (d[2] - c[2]) * r
    return (int(c[0] + dr), int(c[1] + dg), int(c[2] + db))


def bold(msg):
    if not ansi:
        return msg
    return "\033[1m{}\033[0m".format(msg)


def fg(msg, color):
    if not ansi:
        return msg
    return "\033[38;2;{:03};{:03};{:03}m{}\033[0m".format(
        color[0], color[1], color[2], msg
    )


def bg(msg, color):
    if not ansi:
        return msg
    return "\033[48;2;{:03};{:03};{:03}m{}\033[0m".format(
        color[0], color[1], color[2], msg
    )


def color(msg, fgc, bgc):
    return bg(fg(msg, fgc), bgc)


def disp_feed(feed):
    for entry in feed:
        print("-",bold(entry["title"]))
        print(" ",entry["link"])


def disp_summary(user_qa, truncate, sort_key, limit, reverse):
    summary_format = "[{}] {}"
    switch = {
        "reputation": lambda x: -x[1]["score"] * (10 - x[1]["is_accepted"] and 15 or 0),
        "score": lambda x: x[1]["score"],
    }
    if sort_key:
        user_qa.sort(key=switch[sort_key], reverse=reverse)
    if len(user_qa) > limit:
        user_qa = user_qa[:limit]
    for q in [qa[1] for qa in user_qa]:
        votes = fg(q["score"], green) if q["is_accepted"] else q["score"]
        title = (
            (q["title"][: truncate - 3] + "...")
            if len(q["title"]) + 3 > truncate
            else q["title"]
        )
        print(summary_format.format(votes, fg(title, cyan)))


def disp_tags(tags, sort_key, limit):
    width = max(len(x.name) for x in tags) + 23  # for the ansi bytes
    tag_format = "{:>" + str(width) + "} - {:<7.4f}/{:3}"
    alt = True
    switch = {
        "reputation": lambda x: -x.reputation,
        "name": lambda x: x.name,
        "count": lambda x: -x.count,
        "ratio": lambda x: -x.reputation / x.count,
    }
    tags.sort(key=switch.get(sort_key, switch["reputation"]))
    if len(tags) > limit:
        tags = tags[:limit]
    for t in tags:
        print(tag_format.format(fg(t.name, yellow), t.reputation, t.count))
        alt = not alt


def disp_word_freq(word_info, limit=10):
    word_info.sort(key=lambda x: x.frequency, reverse=True)
    if len(word_info) > limit:
        word_info = word_info[:limit]
    print("\n".join(str((x.word, x.frequency)) for x in word_info))


def disp_answer_rated(answer, word_info, tag_info):
    all_words = set(answer.qBody.split())
    word_value = dict()
    for w in all_words:
        v = word_expected_reputation(w, word_info, tag_info)
        word_value[w] = v
    max_value = max(word_value.values())
    ll = [x.split() for x in answer.qBody.split("\n")]
    print(bold(answer.summary.title))
    for l in ll:
        for w in l:
            rel_value = word_value[w] / max_value
            col = (
                gray3
                if rel_value == 0
                else interpolate(darken(yellow, 0.25), magenta, rel_value)
            )
            print(fg(w, col) + " ", end="")
        print()
    print()


def disp_questions(questions):
    for q in questions:
        s = q.summary
        print(fg(s.title, darken(yellow, 0.3)))
        print("\t" + ", ".join([fg(t, darken(cyan, 0.3)) for t in q.tags]))
        print("\t" + s.link)
