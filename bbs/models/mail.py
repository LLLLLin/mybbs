import time
from models import Model
from models.mongo import Mongo
class Mail(Model):
    def __init__(self,form):
        self.id = None
        self.content = form.get('content','')
        self.title = form.get('title','')

        self.ct = int(time.time())
        self.read = False

        self.sender_id = None
        self.receiver_id = int(form.get('to',-1))
    def set_sender(self, sender_id):
        self.sender_id =sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()

class Mail(Mongo):
    __fields__ = Mongo.__fields__ +[
        ('title', str, ''),
        ('content', str, ''),
        ('read', bool, False),
        ('sender_id', int, -1),
        ('receiver_id', int, -1),
    ]
    def set_sender(self, sender_id):
        self.sender_id =sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()