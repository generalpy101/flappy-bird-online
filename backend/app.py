import os

from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit
from flask_migrate import Migrate

from models import db

from views.lobby.view import lobby_bp
from views.player.view import player_bp
from views.scoreboard.view import scoreboard_bp

load_dotenv()

HOST = os.getenv('HOST') or 'localhost'
PORT = os.getenv('PORT') or 3001
DEBUG = os.getenv('DEBUG') or True

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'

io = SocketIO(app, cors_allowed_origins="*")

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(lobby_bp)
app.register_blueprint(player_bp)
app.register_blueprint(scoreboard_bp)

@app.route("/test")
def test():
    return "Hello World!"

if __name__ == '__main__':
    io.run(app, host=HOST, port=PORT, debug=True)