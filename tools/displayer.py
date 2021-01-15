"""Displayer Tool for Answerable

This file contains the functions and variables used to present the data.
"""

import tools.statistics as st

#
# COLOR RELATED VARIABLES AND FUNCTIONS
#
red = (250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)

cyan = (0, 250, 250)
magenta = (250, 0, 250)
yellow = (250, 250, 0)

"""
white = (250, 250, 250)
gray1 = (200, 200, 200)
gray2 = (150, 150, 150)
gray3 = (100, 100, 100)
gray4 = (50, 50, 50)
black = (0, 0, 0)
"""


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


"""
def interpolate(c, d, r):
    dr = (d[0] - c[0]) * r
    dg = (d[1] - c[1]) * r
    db = (d[2] - c[2]) * r
    return (int(c[0] + dr), int(c[1] + dg), int(c[2] + db))
"""

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


def table(data, align=""):
    cols = len(data[0])
    widths = []
    for i in range(0, cols):
        col = [x[i] for x in data]
        widths.append(max([len(str(c)) for c in col]))

    row_f = " ".join(["{{:{}{}}}".format(align, w) for w in widths])
    for d in data:
        print(row_f.format(*d))


def disp_statistics(user_qa):

    ans_f = fg("{}", lighten(blue, 0.3))
    tag_f = fg("[{}]", darken(cyan, 0.2))
    val_f = bold(fg("{}", green))

    def print_section(txt):
        print(bold(txt.upper()))
        print()

    def print_metric(txt):
        def mark(x):
            return bold(x)

        print(mark(txt))

    def print_answer_and_value(answer, value):
        tags = [
            qa[0] for qa in user_qa if qa[0]["question_id"] == answer["question_id"]
        ][0]["tags"]
        print(val_f.format(value), ans_f.format(answer["title"]))
        print(" " * len(str(value)), " ".join([tag_f.format(t) for t in tags]))

    user_answers = [x[1] for x in user_qa]

    print_section("Answer metrics")
    metrics = [
        (bold(k), val_f.format(m(user_answers))) for k, m in st.answer_metrics_single
    ]
    table(metrics)
    print()
    for (name, metric, key) in st.answer_metrics_tops:
        print_metric(name)
        results = metric(user_answers)
        for a in results:
            print_answer_and_value(a, key(a))
        print()

    print_section("Tag metrics")
    for (name, metric) in st.tag_metrics:
        print_metric(name)
        results = metric(user_qa)
        results = [(tag_f.format(r[0]), val_f.format(r[1])) for r in results]
        table(results)
        print()

    print_section("Reputation metrics")
    metrics = [
        (bold(k), val_f.format(m(user_answers)))
        for k, m in st.reputation_metrics_single
    ]
    table(metrics)
    print()
    for w in st.reputation_weight_metrics[0]:
        results = st.reputation_weight_metrics[1](user_answers, w)
        for i, info in enumerate(st.reputation_weight_metrics[2]):
            print_metric(info.format(w * 100))
            print(val_f.format(results[i]))
