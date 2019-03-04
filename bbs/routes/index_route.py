from flask import (
        Blueprint,
        url_for,
        render_template,
        redirect,
        request,
        session,
        send_from_directory,
)

from routes import *


from utils import (log,
                    user_img_director,
                   )

from models.user import User
import os
from  werkzeug.utils import secure_filename



main = Blueprint('index',__name__)









@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['POST'])
def login():

    form = request.form
    user = User.validate_login(form)
    if user is not None:
        session['user_id'] = user.id
        return redirect(url_for('topic.topic_index'))
    else:
        return redirect(url_for('.index'))
@main.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        form = request.form
        u = User.register(form)
        return redirect(url_for('.index'))
    return render_template('register.html')
@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html',user=u)


@main.route('/addimg',methods=['POST'])
def add_img():
    u = current_user()
    file = request.files['file']
    filename = file.filename
    if filename == '':
            return redirect(request.url)
    if allow_file(filename):
        filename = secure_filename(filename)
        file.save(os.path.join(user_img_director,filename))
        u.user_image = filename
        u.save()
    return redirect(url_for(".profile"))


@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(user_img_director,filename)