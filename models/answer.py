import json

from models.summary import Summary

class Answer:
    def __init__(self, summary, qBody, aBody, tags):
        self.summary = summary
        self.qBody = qBody
        self.aBody = aBody
        self.tags = tags
    def __str__(self):
        return '# {}\n{}\n***\n{}\n{}'.format(
            self.summary.title,
            self.qBody,
            self.tags,
            self.aBody
            )
    def toJSON(self):
        return json.dumps({
            'summary':self.summary.toMap(),
            'qBody':self.qBody,
            'aBody':self.aBody,
            'tags':self.tags
            })
    
    def fromMap(obj):
        sumry = obj['summary']
        return Answer(
            Summary(
                sumry['title'],
                sumry['votes'],
                sumry['accepted'],
                sumry['link']
                ),
            obj['qBody'],
            obj['aBody'],
            obj['tags']
            )
