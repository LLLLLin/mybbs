from flask import(
        Blueprint,
        render_template,
        request,
        redirect,
        url_for,
)

from models.board import  Board


main = Blueprint('board', __name__)

#TODO:添加权限后管理员才能登陆
@main.route('/admin')
def board_index():
    return render_template('board/admin_index.html')

@main.route('/add', methods=['POST'])
def add_board():
    form = request.form
    b = Board.new(form)
    b.save()
    return redirect(url_for('topic.topic_index'))