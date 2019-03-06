from flask import(
    render_template,
    request,
    redirect,
    Blueprint,
    url_for,
)

from routes import *

from models.reply import Reply

main = Blueprint('reply',__name__)

@main.route('/add', methods=["POST"])
def reply_add():
    form = request.form
    u = current_user()
    m = Reply.new(form)
    m.set_user_id(u.id)
    m.save()
    return redirect(url_for('topic.topic_detail' ,id = m.topic_id))