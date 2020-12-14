import sys

from tools import fetcher

if (len(sys.argv) == 1):
    print('Introduce user')
    exit()

user_id = sys.argv[1]

summaries = fetcher.get_summaries(user_id);

print('\n'.join([str(a) for a in summaries]))
