from flask import (Blueprint,
                   render_template,
                   url_for,
                   request,
                   redirect,
)

from routes import *

from models.mail import Mail

main = Blueprint('mail',__name__)

@main.route('/', methods=['GET'])
def mail_index():
    u = current_user()
    send_mail = Mail.find_all(sender_id = u.id)
    received_mail = Mail.find_all(receiver_id = u.id)
    return render_template('mail/index.html', sends = send_mail, receives = received_mail)

@main.route('/<int:id>')
def mail_view(id):
    mail = Mail.find(id)
    if current_user().id in [mail.receiver_id, mail.sender_id]:
        if current_user().id == mail.receiver_id:
            mail.mark_read()
        return render_template('mail/detail.html',mail = mail)
    else:
        return redirect(url_for('.mail_index'))

@main.route('/add', methods=['POST'])
def mail_add():
    form = request.form
    receiver = form.get('receiver','')
    u =User.find_by(username = receiver)
    mail = Mail.new(form,receiver_id = u.id)
    mail.set_sender(current_user().id)
    mail.save()
    return redirect(url_for('.mail_index'))