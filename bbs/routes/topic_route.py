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
        board_id = int(request.args.get('board_id', -1))
        if board_id == -1:
            tops = Topic.all()
        else:
            tops = Topic.find_all(board_id=board_id)
            log('debug', tops)
        boards = Board.all()
        # log('debug',tops[0].user().user_img)
        return render_template('topic/index.html', bs=boards, ms=tops)

@main.route('/<int:id>')
def topic_detail(id):
    topic = Topic.get(id)
    return render_template('topic/detail.html',topic = topic)

@main.route('/add', methods=['POST'])
def topic_add():
    u = current_user()
    form = request.form
    topic = Topic.new(form,user_id=u.id)
    return redirect(url_for('.topic_detail',id = topic.id))
#TODO:管理员才能访问
@main.route('/delete')
def topic_delete():
    query = request.args
    topic_id = query.get('id', -1)
    topic = Topic.delete(id = topic_id)
    return redirect(url_for('.topic.index'))

@main.route('/new')
def topic_new():
    u =current_user()
    boards = Board.all()
    return render_template('topic/new.html',bs = boards,user = u)