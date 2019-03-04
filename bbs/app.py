from flask import (Flask,
                    blueprints,
                   )

from routes.board_route import main as board
from routes.mail_route import  main as mail
from routes.reply_route import  main as reply
from routes.index_route import  main as index
from routes.topic_route import main as topic
app = Flask(__name__)
app.secret_key = 'dasfjaldshfdoshdf'
app.register_blueprint(index)
app.register_blueprint(topic,url_prefix='/topic')
app.register_blueprint(board,url_prefix='/board')
app.register_blueprint(reply,url_prefix='/reply')
app.register_blueprint(mail, url_prefix='/mail')

if __name__ == '__main__':

    config ={
        'debug': True,
        'host' : '0.0.0.0',
        'port': 3000,
    }
    app.run(**config)
