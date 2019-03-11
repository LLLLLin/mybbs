from flask import(
        render_template,
        request,
        redirect,
        url_for,
        Blueprint,
)

from routes import *

from models.topic import Topic
from models.board import Board


from utils import log


main = Blueprint('topic', __name__)







@main.route('/')
def topic_index():
        log('topic_index:', request.method, request.form, request.path)
        u = current_user()
        if u == None:
            return redirect(url_for('index.index'))
        board_id = int(request.args.get('board_id', -1))
        if board_id == -1:
            tops = Topic.all()
        else:
            tops = Topic.find_all(board_id=board_id)
            log('debug', tops)
        boards = Board.all()
        # log('debug',tops[0].user().user_img)
        return render_template('topic/index.html', bs=boards, ms=tops, u = u)

@main.route('/<int:id>')
def topic_detail(id):
    u = current_user()
    if u == None:
        return redirect(url_for('index.index'))
        return redirect(url_for('index.index'))
    topic = Topic.get(id)
    return render_template('topic/detail.html',topic = topic)

@main.route('/add', methods=['POST'])
def topic_add():
    u = current_user()
    if u == None:
        return redirect(url_for('index.index'))
    form = request.form
    topic = Topic.new(form,user_id=u.id)
    topic.save()
    return redirect(url_for('.topic_detail',id = topic.id))
#TODO:管理员才能访问
@main.route('/delete')
def topic_delete():
    u =current_user()
    if u == None:
        return redirect(url_for('index.index'))
    query = request.args
    topic_id = query.get('id', -1)
    topic = Topic.delete(id = int(topic_id))
    return redirect(url_for('.topic_index'))

@main.route('/new')
def topic_new():
    u =current_user()
    if u == None:
        return redirect(url_for('index.index'))
    boards = Board.all()
    return render_template('topic/new.html',bs = boards,user = u)