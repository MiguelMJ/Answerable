import sys
import json
import argparse
import pathlib
import datetime
import textwrap

from tools import fetcher, displayer, recommender, log

_config_file = ".config"
log_who = "Answerable"


def get_user_tags(args):
    """Return the tags if the args contain the tags file

    If the user used the -t option, parse the specified file. Otherwise,
    return None
    """

    if args.tags is not None:
        return fetcher.get_user_tags(args.tags)
    else:
        log.log(log_who, "No tags file provided.")
        return None


def load_config(args) -> dict:
    """Return the user configuration

    If the _config_file exists, return its contents. Otherwise, extact the
    the configuration from the options -u and -t
    """

    try:
        fh = open(_config_file)
        config = json.load(fh)
    except IOError:
        if args.user == None:
            log.log(log_who, ".config not found: provide user id with -u option")
            exit(1)
        config = {"user": args.user, "tags": get_user_tags(args)}
    finally:
        fh.close()
    return config


def save_config(args):
    """Store the user configuration

    Create or overwrite the confguration file with the configuration extracted
    from the options -u and -t.
    """

    with open(_config_file, "w") as fh:
        tags = get_user_tags(args)
        json.dump({"user": args.user, "tags": tags}, fh, indent=2)
        log.log(log_who, "Configuration saved in {}", _config_file)


def summary(args):
    """Display a summary of the answered questions"""

    config = load_config(args)
    qa = fetcher.get_QA(config["user"])
    displayer.disp_summary(
        qa,
        truncate=args.max_line,
        sort_key=args.key,
        limit=args.limit,
        reverse=args.reverse,
    )


def recommend(args):
    """Recommend questions from the latest unanswered"""

    # Load configuration, get user info and feed
    config = load_config(args)
    user_qa = fetcher.get_QA(config["user"])
    if config["tags"] is None:
        tags = ""
    else:
        tags = "tag?tagnames="
        tags += "%20or%20".join(config["tags"]["followed"]).replace("+", "%2b")
        tags += "&sort=newest"
    url = "https://stackoverflow.com/feeds/" + tags
    feed = fetcher.get_question_feed(url)
    # with open("data/test/feed.json") as fh:
    #     feed = json.load(fh)
    #     feed = [x for x in feed
    #             if len(set(x["tags"]) & set(config["tags"]["followed"])) > 0]

    # Filter feed from ignored tags
    hide_tags = set(config["tags"]["ignored"])

    def should_show(entry):
        # True if empty intersection
        return len(set(entry["tags"]) & hide_tags) == 0

    feed = [e for e in feed if should_show(e)]

    rec_index = recommender.recommend(user_qa, feed)
    selection = [feed[i] for i in rec_index[: args.limit]]
    displayer.disp_feed(selection)
    pass


def parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments

    Parse sys.argv into a Namespace, that will be used in the rest of the
    functions.
    """

    parser = argparse.ArgumentParser(
        usage="%(prog)s COMMAND [OPTIONS]",
        description="Stack Overflow unanswered questions recommendation system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
                For more information, see the README.md
                The code for Answerable is available in https://github.com/MiguelMJ/Answerable
                """
        ),
    )
    parser.add_argument(
        "command",
        choices=("save", "summary", "tags", "answers", "recommend"),
        help="save,summary,tags,answers,recommend",
        default=None,
        metavar="COMMAND",
    )
    parser.add_argument("-r", "--reverse", help="reverse sorting", action="store_true")
    parser.add_argument(
        "-u", "--user", help="identifier of Stack Overflow user", metavar="ID"
    )
    parser.add_argument(
        "-l",
        "--limit",
        help="limit the number of items displayed",
        type=int,
        default=999,
        metavar="N",
    )
    parser.add_argument(
        "-m",
        "--max-line",
        help="truncate titles with a max length in <summary>",
        type=int,
        default=80,
        metavar="N",
    )
    parser.add_argument(
        "-k",
        "--key",
        help="sort the items displayed to a given key. It has no effect on <recommend>",
        default=None,
        metavar="K",
    )
    parser.add_argument(
        "-a",
        "--all",
        help="search through all the new questions, without tag filter. If the user tags haven't been saved before with the <save> command, this option is on by default",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--tags",
        help="file with the source of the page with the user followed and ignored tags",
        metavar="FILE",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Show the log content in stderr too",
        action="store_true",
    )
    parser.add_argument("--no-ansi", help="print without colors", action="store_true")
    args = parser.parse_args()
    if args.no_ansi:
        displayer.ansi = False
    return args


if __name__ == "__main__":
    switch = {
        "save": save_config,
        "summary": summary,
        "recommend": recommend,
    }
    args = parse_arguments()
    command = args.command

    log.add_log("answerable.log")
    if args.verbose:
        log.add_stderr()

    log.log(log_who, displayer.bold("Log of {}"), datetime.datetime.now())

    switch[command](args)

    log.close_logs()
