import os

from flask import Flask, redirect, url_for
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user

from models import db
from models.user import User

load_dotenv()

HOST = os.getenv("HOST") or "localhost"
PORT = os.getenv("PORT") or 3000
DEBUG = os.getenv("DEBUG") or True

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///scores.db"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

login_manager = LoginManager()

db.init_app(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

app.app_context().push()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("auth.login")


@app.route("/")
@login_required
def index():
    if current_user.is_admin:
        return redirect(url_for("admin.list_lobbies"))
    else:
        return redirect(url_for("player.join_lobby"))

@app.route("/test")
def test():
    return "Hello World!"


from views.auth.routes import auth_bp
from views.player.routes import player_bp
from views.admin.routes import admin_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(player_bp, url_prefix="/player")

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)
