from models import Model
from models.mongo import  Mongo


# class User(Model):
#     def __init__(self, form):
#         self.id = form.get('id', None)
#         self.username = form.get('username', '')
#         self.password = form.get('password', '')
#         self.user_img = 'default.png'
#
#     # 密码加盐
#     def salted_password(self, password, salt='$!@><?>HUI&DWQa'):
#         import hashlib
#         def sha256(ascii_str):
#             return hashlib.sha256(ascii_str.encode('ascii')).Hexdigest()
#
#         hash1 = sha256(password)
#         hash2 = sha256(hash1 + salt)
#         return hash2
#
#     # 用户注册检测
#     def register(self, form):
#         name = form.get('username', '')
#         passwd = form.get('password', '')
#         if len(name) > 2 and User.find_by(username=name) is None:
#             u = User.new(form)
#             u.password = u.saled_password(passwd)
#             u.save()
#             return u
#
#     # 登陆注册
#     def validate_login(self, form):
#         u = User(form)
#         user = User.find_by(username=u.username)
#         if user is not None and user.password == u.salted_password(u.password):
#             return user
#         else:
#             return None
class User(Mongo):
        __fields__ = Mongo.__fields__+[
            ('username', str, ''),
            ('password', str, ''),
            ('user_image', str, 'default.png'),
        ]

        # 密码加盐
        def salted_password(self, password, salt='$!@><?>HUI&DWQa'):
            import hashlib
            def sha256(ascii_str):
                return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

            hash1 = sha256(password)
            hash2 = sha256(hash1 + salt)
            return hash2

        # 用户注册检测
        @classmethod
        def register(cls, form):
            name = form.get('username', '')
            passwd = form.get('password', '')
            if len(name) > 2 and User.find_by(username=name) is None:
                u = User.new(form)
                u.password = u.salted_password(passwd)
                u.save()
                return u
            # 登陆注册
        @classmethod
        def validate_login(self, form):
              u = User.new(form)
              user = User.find_by(username=u.username)
              if user is not None and user.password == u.salted_password(u.password):
                         return user
              else:
                         return None