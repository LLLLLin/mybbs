from flask import  session
from models.user import User
from utils import accept_file_type
def current_user():
    uid = session.get('user_id',-1)
    u = User.find_by(id = uid)
    return u

def allow_file(filename):
    suffix =filename.split('.')[-1]
    return suffix in accept_file_type