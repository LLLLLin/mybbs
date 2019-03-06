from pymongo import MongoClient
from time import time
from utils import log
mongo =  MongoClient()
def next_id(name):
    query ={
        'name': name,
    }
    update = {
        '$inc':{
            'seq':1,
        }
    }
    kwargs ={
        'query':query,
        'update':update,
        'upsert':True,
        'new': True,
    }
    doc = mongo.db['data_id']
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id
class Mongo:
    __fields__ =[
        '_id',
        ('id', int, -1),
        ('type', str,''),
        ('ct', int, 0),
        ('ut', int, 0),
    ]
    @classmethod
    def has(cls, **kwargs):
        return cls.find_by(kwargs) is not None

    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def new(cls, form = None, **kwargs):
        name = cls.__name__
        m = cls()
        __field__ = cls.__fields__.copy()
        __field__.remove('_id')
        if form is None:
            form = {}
        for f in __field__ :
            k, t, v = f
            if k in form :
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k , v)
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v )
            else:
                raise KeyError
        m.id = next_id(name)
        ts = int(time())
        m.ct = ts
        m.ut = ts
        m.type = name.lower()
       # m.save()
        return m


    @classmethod
    def find_all(cls,**kwargs):
        return cls._find(**kwargs)


    @classmethod
    def find_by(cls,**kwargs):
        ms = cls._find(**kwargs)
        if len(ms) > 0:
            log('debug', ms[0])
            return ms[0]
        return None


    @classmethod
    def find(cls,id):
        return cls.find_by(id=id)

    @classmethod
    def upsert(cls,query_form,update_form,hard = False):
        ms = cls.find_by(**query_form)
        if ms is  None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard= hard)
        return ms


    def update(self, form, hard= False):
        for k, v in form.iteams():
            if hard or hasattr(self, k):
                setattr(self,k , v)
        self.save()

    @classmethod
    def _clean_field(cls,source, target):
        ms = cls._find()
        for m in ms:
            value = getattr(m,source)
            setattr(m,target,value)
            m.save()


    @classmethod
    def _find_row(cls,**kwargs):
        name = cls.__name__
        ms = mongo.db[name].find(kwargs)
        ms = [m for m in ms]
        return ms


    @classmethod
    def _new_with_bson(cls,bson):
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, t(bson[k]))
            else:
                setattr(m, k, v)
            setattr(m, '_id', bson['_id'])
        return m


    @classmethod
    def _find(cls,**kwargs):
        name=cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = mongo.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    def save(self):
        name = self.__class__.__name__
        mongo.db[name].save(self.__dict__)
    def json(self):
        data = self.__dict__
        d = {k: v for k, v in data.items() if k not in ['_id']}
        return d
    def data_count(self, cls):
        name = cls.__name__
        find_key = '{}_id'.format(self.type)
        query ={
            find_key: self.id,
        }
        count = mongo.db[name].find(query).count()
        return count
    def __repr__(self):
        name = self.type
        properties = ('{} = {}'.format(k,v) for k, v in self.__dict__.items())
        return '<{}:\n {}\n>'.format(name,'\n'.join(properties))