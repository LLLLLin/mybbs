from models  import Model
import time
from .reply import Reply
from models.mongo import Mongo
import json
from .board import Board
from .user import User

from utils import log

class Topic(Model):
    def __init__(self, form):
        self.id = None
        self.views = 0
        self.title = form.get('title','')
        self.content = form.get('content','')
        self.ct = int(time.time())
        self.ut = self.ct
        self.user_id = form.get('user_id','')
        self.cter = form.get('creater','')
    def replies(self):
        u = Reply.find(self.id)
        return u

class Topic(Mongo):
    __fields__ =  Mongo.__fields__+[
        ('content', str, ''),
        ('title', str, ''),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('views', int, 0),
    ]
    @classmethod
    def get(cls, id):
        topic = cls.find(id)
        topic.views += 1
        topic.save()
        return topic
    def to_json(self):
        d = dict()
        for k in Topic.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self.key)
        return json.dumps(d)

    @classmethod
    def to_obj(cls, j):
        d = json.loads(j)
        m = cls()
        for k,v in d.items():
            setattr(m, k, v)
        return isinstance(

        )
    def replies(self):
        ms = Reply.find_all(topic_id = self.id)
        return ms

    def boards(self):
        bs = Board.find(self.board_id)
        return bs
    def user(self):
        u = User.find(self.user_id)
        return u