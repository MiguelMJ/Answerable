import sys

from tools import fetcher, displayer, analyzer


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("usage: python answerable.py <user_id> [summary|tags|answers|usertags]")
    exit()

user_id = sys.argv[1]
option = sys.argv[2] if len(sys.argv) == 3 else "questions"
ans = fetcher.get_answers(user_id)
tag_info = analyzer.tag_info(ans)
word_info = analyzer.word_info(ans)

if option == "summary":
    displayer.disp_summary([x.summary for x in ans])
elif option == "tags":
    displayer.disp_tags(list(tag_info.values()))
elif option == "answers":
    for a in ans:
        displayer.disp_answer_rated(a, word_info, tag_info)
elif option == "questions":
    questions = fetcher.get_tagged_question_feed(["c++", "java", "python"])
    vq = [
        (analyzer.answer_expected_reputation(q, word_info, tag_info), q)
        for q in questions
    ]
    vq.sort(reverse=True)
    displayer.disp_questions([q for (v, q) in vq[:10]])
elif option == "usertags":
    t = fetcher.get_user_tags("source.html")
    print("FOLLOWED")
    print("\n".join(t["followed"]))
    print("IGNORED")
    print("\n".join(t["ignored"]))
else:
    print("Unknown option", option)

# Code to compare expected vs real reputation
#
# ans.sort(key=lambda x:(x.summary.reputation,x.summary.title), reverse=True)
# reality = [(a.summary.title[:25],a.summary.reputation) for a in ans]
# expectations = [(analyzer.answer_expected_reputation(x,word_info,tag_info),x.summary.title) for x in ans]
# expectations.sort(reverse=True)
# expectations = [(y[:25],x) for (x,y) in expectations]
# for x in zip(reality,expectations):
#    print(x)
