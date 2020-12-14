class Summary:
    accepted_color = '\033[38;2;0;250;0m'
    title_color = '\033[38;2;0;0;250m'
    summary_format = "[{}{}\033[0m] {}{}\033[0m"
    title_truncate = 50
    
    def __init__(self, title, votes, accepted, link):
        self.title = title
        self.votes = votes
        self.link = link
        self.identifier = link[link.rfind('#')+1:]
        self.accepted = accepted
        self.reputation = votes * 10 + accepted * 15
    
    def __str__(self) -> str:
        return Summary.summary_format.format(
            Summary.accepted_color if self.accepted else '',
            self.votes,
            Summary.title_color,
            (self.title[:Summary.title_truncate]+'...') if len(self.title)>Summary.title_truncate else self.title)
