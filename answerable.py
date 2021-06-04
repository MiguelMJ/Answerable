import re
import json
import argparse
import datetime
import textwrap
import importlib

from urllib.error import URLError

from tools import fetcher, displayer, log, spider

_current_version = "v1.1"


def latest_version():
    try:
        res = spider.get(
            "https://api.github.com/repos/MiguelMJ/Answerable/releases/latest", 0
        )
        if res.status_code != 200:
            log.warn("Unable to get information from latest version")
            return None
        latest = re.search(r"v[\d.]+.?", json.loads(res.content)["name"])[0]
        return latest
    except URLError:
        log.warn("Unable to get information from latest version")
    return None


_config_file = ".config"


def get_user_tags(args):
    """Return the tags if the args contain the tags file

    If the user used the -t option, parse the specified file. Otherwise,
    return None
    """

    if args.tags is not None:
        return fetcher.get_user_tags(args.tags)
    else:
        log.log("No tags file provided.")
        return None


def load_config(args) -> dict:
    """Return the user configuration

    If the _config_file exists, return its contents. Otherwise, extract the
    the configuration from the options -u, -t and -m
    """

    try:
        with open(_config_file) as fh:
            file_config = json.load(fh)
    except IOError:
        file_config = {}
    finally:
        default_config = {"model": "content_based_1"}
        cli_config = {"user": args.user, "tags": args.tags, "model": args.model}
        cli_config = {k: v for k, v in cli_config.items() if v is not None}
        config = {**default_config, **file_config, **cli_config}
        if config["user"] is None:
            log.abort(".config not found: provide user id with -u option")
    return config


def save_config(args):
    """Store the user configuration

    Create or overwrite the configuration file with the configuration extracted
    from the options -u and -t.
    """

    with open(_config_file, "w") as fh:
        tags = get_user_tags(args)
        json.dump(
            {"user": args.user, "tags": tags, "model": args.model or "content_based_1"},
            fh,
            indent=2,
        )
        log.log("Configuration saved in {}", _config_file)


def summary(args):
    """Display a summary of the answered questions"""

    config = load_config(args)
    qa = fetcher.get_QA(config["user"], force_reload=args.f)
    qa = [(q, a) for q, a in qa if a is not None]
    displayer.disp_statistics(qa)


def recommend(args):
    """Recommend questions from the latest unanswered"""

    filtered = {"hidden": 0, "closed": 0, "duplicate": 0, "answered": 0}
    present = set()
    def valid_entry(entry):
        """Check if a entry should be taken into account"""
        
        title = entry["title"]
        if title in present:
            return False
        present.add(title)
        if len(set(entry["tags"]) & hide_tags) > 0:
            filtered["hidden"] += 1
            log.log("hidden: {}", title)
            return False
        if title[-8:] == "[closed]":
            filtered["closed"] += 1
            log.log("closed: {}", title)
            return False
        if title[-11:] == "[duplicate]":
            filtered["duplicate"] += 1
            log.log("duplicate: {}", title)
            return False
        if entry["accepted_answer_id"] is not None or config["user"] in {x["owner"]["user_id"] for x in entry["answers"]}:
            filtered["answered"] += 1
            log.log("answered: {}", title)
            return False
        return True

    def cf(x):
        """Color a value according to its value"""

        return (
            displayer.fg(x, displayer.green)
            if x == 0
            else displayer.fg(x, displayer.magenta)
        )

    # Load configuration
    config = load_config(args)

    # Load the model
    try:
        model_name = config["model"]
        log.log("Loading model {}", displayer.fg(model_name, displayer.yellow))
        model = importlib.import_module(f".{model_name}", "models")
        log.log(
            "Model {} succesfully loaded", displayer.fg(model_name, displayer.green)
        )
    except ModuleNotFoundError as err:
        if err.name == f"models.{model_name}":
            log.abort("Model {} not present", model_name)
        else:
            log.abort("Model {} unsatisfied dependency: {}", model_name, err.name)

    # Get user info and feed
    user_qa = fetcher.get_QA(config["user"], force_reload=args.f)
    try:
        
        if args.all or "tags" not in config:
            feed = fetcher.get_question_feed([""], force_reload=args.F)
        else:
            tags = [x.replace("+", "%2b") for x in config["tags"]["followed"]]
            feed = fetcher.get_question_feed(tags, force_reload=args.F)
        if len(feed) == 0:
            raise ValueError("No feed returned")
        # Filter feed from ignored tags
        hide_tags = (
            set()
            if args.all or "tags" not in config
            else set(config["tags"]["ignored"])
        )
        useful_feed = [e for e in feed if valid_entry(e)]
        if len(useful_feed) == 0:
            raise ValueError("All feed filtered out")
        log.log(
            "Discarded: {} ignored | {} closed | {} duplicate | {} answered",
            cf(filtered["hidden"]),
            cf(filtered["closed"]),
            cf(filtered["duplicate"]),
            cf(filtered["answered"]),
        )

        # Make the recommendation
        log.log(f"Corpus size: {len(user_qa)} Feed size: {len(useful_feed)}")
        rec_index, info = model.recommend(user_qa, useful_feed)
        selection = [useful_feed[i] for i in rec_index[: args.limit]]
        if args.info and info is None:
            log.warn("Info requested, but model {} returns None", model_name)
        elif args.info and info is not None:
            info = [info[i] for i in rec_index[: args.limit]]
        displayer.disp_feed(selection, info, args.info)
    except ValueError as err:
        log.warn(err)
        log.print_advice()


def parse_arguments() -> argparse.Namespace:
    """Parse the command line arguments

    Parse sys.argv into a Namespace, that will be used in the rest of the
    functions.
    """

    parser = argparse.ArgumentParser(
        usage="%(prog)s COMMAND [OPTIONS]",
        description=f"Answerable {_current_version}\nStack Overflow unanswered questions recommendation system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """\
                Code: https://github.com/MiguelMJ/Answerable
                Documentation: in https://github.com/MiguelMJ/Answerable/wiki
                """
        ),
    )
    parser.add_argument(
        "command",
        choices=("save", "summary", "recommend"),
        help="save,summary,recommend",
        metavar="COMMAND",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="show the log content in stderr too",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--info",
        help="print extra info on each recomendation",
        action="store_true",
    )
    parser.add_argument("--no-ansi", help="print without colors", action="store_true")
    parser.add_argument("-f", help="force reload of user data", action="store_true")
    parser.add_argument(
        "-F", help="force retrieval of question feed", action="store_true"
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
        "-a",
        "--all",
        help="don't use tags to filter the feed. If the user tags haven't been saved before with the <save> command, this option is on by default",
        action="store_true",
    )
    parser.add_argument(
        "-u", "--user", help="identifier of Stack Overflow user", metavar="ID"
    )
    parser.add_argument(
        "-t",
        "--tags",
        help="file with the source of the page with the user followed and ignored tags",
        metavar="FILE",
    )
    parser.add_argument(
        "-m",
        "--model",
        help="specify the recommendation model you want to use",
        metavar="MODEL",
    )
    args = parser.parse_args()
    if args.no_ansi:
        displayer.ansi = False
    return args


if __name__ == "__main__":
    _latest_version = latest_version()
    if _latest_version is not None and _latest_version != _current_version:
        log.warn(
            f"New version on GitHub: {_latest_version} (current is {_current_version})"
        )
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

    log.log(displayer.bold("Log of {}"), datetime.datetime.now())

    switch[command](args)

    log.close_logs()
