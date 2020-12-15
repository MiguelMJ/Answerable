red   = (250,0,0)
green = (0,250,0)
blue  = (0,0,250)

cyan    = (0,250,250)
magenta = (250,0,250)
yellow  = (250,250,0)

white = (250,250,250)
gray1 = (200,200,200)
gray2 = (150,150,150)
gray3 = (100,100,100)
gray4 = (50,50,50)
black = (0,0,0)

def bold(msg):
    return '\033[1m{}\033[0m'.format(msg)
def fg(msg, color):
    return '\033[38;2;{:03};{:03};{:03}m{}\033[0m'.format(
                                            color[0],
                                            color[1],
                                            color[2],
                                            msg)
def bg(msg, color):
    return '\033[48;2;{:03};{:03};{:03}m{}\033[0m'.format(
                                            color[0],
                                            color[1],
                                            color[2],
                                            msg)
def color(msg,fgc,bgc):
    return bg(fg(msg,fgc),bgc)

def disp_summary(summaries, truncate=80, sort_key='reputation', limit=50):
    summary_format = '[{}] {}'
    switch = {
        'reputation':lambda x: x.reputation,
        'votes':lambda x: x.votes
    }
    summaries.sort(key=switch.get(sort_key,None), reverse=True)
    if len(summaries) > limit:
        summaries = summaries[:limit]
    for s in summaries:
        votes = fg(s.votes, green) if s.accepted else s.votes
        title = (s.title[:truncate-3]+'...') if len(s.title)+3 > truncate else s.title
        print(summary_format.format(
                    votes,
                    fg(title, cyan)
                )
             )

def disp_tags(tags, sort_key='ratio', limit=15):
    width = max(len(x.name) for x in tags) + 23 # for the ansi bytes
    tag_format = '{:>'+str(width)+'} - {:<7.4f}/{:3}'
    alt = True
    switch = {
        'reputation':lambda x: -x.reputation,
        'name':lambda x: x.name,
        'count':lambda x: -x.count,
        'ratio':lambda x: -x.reputation/x.count,
    }
    tags.sort(key=switch.get(sort_key,None))
    if len(tags) > limit:
        tags = tags[:limit]
    for t in tags:
        print(tag_format.format(
                    fg(t.name, yellow),
                    t.reputation,
                    t.count
                )
             )
        alt = not alt
        
def disp_word_freq(word_info, limit=10):
    word_info.sort(key=lambda x: x.frequency, reverse=True)
    if len(word_info) > limit:
        word_info=word_info[:limit]
    print('\n'.join(str((x.word, x.frequency)) for x in word_info))
    
