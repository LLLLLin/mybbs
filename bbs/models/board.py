import time
from models import Model

from models.mongo import Mongo

class Board(Model):
    def __init__(self,form):
        self.id =  None
        self.title = form.get('title','')
        self.ct = int(time.time())
        self.ut = self.ct

class Board(Mongo):
    __fields__ = Mongo.__fields__+[
        ('title', str, '')
    ]