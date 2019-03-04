import json

#向磁盘写入文件
def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)

#从磁盘读取数据
def load(path):
    with open(path,"r", encoding='utf-8') as f:
        s = f.read()
        return json.loads(s)


# 数据ORM 所有数据类的基类
class Model(object):

    @classmethod
    def db_path(cls):
        #通过数据类类名获取数据本地文件路径的类方法
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)

    @classmethod
    def all(cls):
        #获取数据文件中所有的数据,并返回一个所有数据实例的列表
        path = cls.db_path()
        models = load(path)
        ms = [cls._new_from_dict() for m in models]
        return ms
    #保存数据
    #TODO:当前方法每更新添加一个新数据都需要将数据文件中所有数据拿出，可以改进存储方式
    def save(self):
        models = self.all()
        if self.id is None: #如果当前实例为新创建
            if len(models) == 0:#且数据文件中没有数据
                self.id = 0#将当前实例id属性置0
            else:#如果数据文件中有数据
                m = models[-1]
                self.id = m.id+1#将数据文件中最后一个数据的id属性+1作为当前实例的id属性
            models.append(self)
        else:#如果是更新数据
            index = -1
            for i, m in enumerate(models):#enumerate函数将生成一个[(index:项)]的列表找到与更新实例id属性相同的数据，并替代它
                if m.id == self.id:
                    index = i
                    break
            models[index] = self
        l = [m.__dict__ for m in models]
        path  =self.db_path()
        save(l, path)
    def _new_from_dict(cls, d):
        #为类添加新属性
        m = cls({})
        for k, v in d.items():
            setattr(m, k, v)
        return m

    def json(self):
        #将当前实例json格式化 实例属性组成的字典
        d = self.__dict__.copy()
        return d

    @classmethod
    def new(cls,form, **kwargs):
        #创建新的类实例，并可通过指定参数添加类属性,返回当前实例
        m = cls(form)
        for k, v in kwargs.items():
            setattr(m, k, v)
        m.save()
        return m
    @classmethod
    def find_all(cls, **kwargs):
        #通过多组参数查找匹配的所有数据
        #TODO:当前逻辑有BUG 只能匹配最后一组给定参数吻合数据
        ms=[]
        k, v = '',''
        for key, value in kwargs.items():
            k, v = key,value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                ms.append(m)
        return ms
    @classmethod
    def find_by(cls, **kwargs):
        #通过多组参数查找匹配的第一组数据
        # TODO:当前逻辑有BUG 只能匹配最后一组给定参数吻合数据
        k, v ='',''
        for key, value in kwargs.items():
            k,v = key, value
        all = cls.all()
        for m in all:
            if v == m.__dict__[k]:
                return m
        return None
    @classmethod
    def find(cls,id):
        #通过id查找数据文件中匹配的第一组数据
        return cls.find_by(id)

    @classmethod
    def delete(cls,id):
        #删除id指定的数据 并返回该数据
        models = cls.all()
        index = -1
        for i,e in enumerate(models):
            if e.id == id:
                index = i
                break
        if index == -1:
            pass
        else:
            obj = models.pop(index)
            l = [m.__dict__ for m in models]
            path = cls.db_dbpah()
            save(l, path)
            return obj

    def __repr__(self):
        #重新定义model对象print输出格式
        classname = self.__class__.__name__
        properties = ['{}:({})'.format(k,v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '<{}\n{} \n>\n'.format(classname,s)