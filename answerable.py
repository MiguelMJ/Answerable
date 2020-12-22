import sys
import json
import argparse
import textwrap

from tools import fetcher, displayer, analyzer

def save(args):
    with open(".config","w") as fh:
        tags = fetcher.get_user_tags(args.tags_file)
        json.dump({
                "user": args.user,
                "tags": tags
            },
            fh)

def summary():
    pass

def tags():
    pass

def answers():
    pass

def questions():
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Stack Overflow unanswered questions recommendation system",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=textwrap.dedent("""\
                For more information, see the README.md
                The code for Answerable is available in https://github.com/MiguelMJ/Answerable
                """)
        )
    
    parser.add_argument("command",
                        choices=(
                            "save",
                            "summary",
                            "tags",
                            "answers",
                            "questions"
                        ),
                        help="save,summary,tags,answers,questions", 
                        metavar="COMMAND")
    parser.add_argument("-r","--reverse", 
                        help="reverse sorting", 
                        action="store_true")
    parser.add_argument("-u","--user", 
                        help="identifier of Stack Overflow user",
                        metavar="ID")
    parser.add_argument("-l","--limit", 
                        help="limit the number of items displayed",
                        type=int,
                        default=15,
                        metavar="N")
    parser.add_argument("-m","--max-line", 
                        help="truncate titles with a max length in <summary>",
                        type=int,
                        default=80,
                        metavar="N")
    parser.add_argument("-k","--key", 
                        help="sort the items displayed to a given key. It has no effect on <questions>",
                        choices=(
                            "date",
                            "count",
                            "score",
                            "value",
                            "reputation"
                        ),
                        default="date",
                        metavar="K")
    parser.add_argument("-a","--all", 
                        help="search through all the new questions, without tag filter. If the user tags haven't been saved before with the <save> command, this option is on by default.",
                        action="store_true")
    parser.add_argument("-t","--tags",
                        help="file with the source of the page with the user followed and ignored tags",
                        metavar="FILE")
    parser.add_argument("--no-ansi", 
                        help="print without colors",
                        action="store_true")
    args = parser.parse_args()
    if args.no_ansi:
        displayer.ansi = False
    return args

if __name__ == "__main__":
    switch = {
        "save":save,
        "summary":summary,
        "tags":tags,
        "answers":answers,
        "questions":questions,
    }
    args = parse_arguments()
    command = args.command
    switch[command](args)
