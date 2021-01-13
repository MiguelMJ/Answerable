"""Displayer Tool for Answerable

This file contains the functions and variables used to present the data.
"""

#
# COLOR RELATED VARIABLES AND FUNCTIONS
#
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


#
# ANSI RELATED VARIABLES AND FUNCTIONS
#
ansi = True


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


#
# DATA DISPLAY FUNCTIONS
#
def disp_feed(feed):
    for entry in feed:

        def title(x):
            return fg(bold(x), lighten(blue, 0.3))

        def tag(x):
            return fg("[" + x + "]", darken(cyan, 0.2))

        print("o", title(entry["title"]))
        print(" ", " ".join(tag(t) for t in entry["tags"]))
        print(" ", entry["link"])


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
