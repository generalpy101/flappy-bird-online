from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from models.user import User
from models.lobby import Lobby
from models.score import Score
from models import db

player_bp = Blueprint("player", __name__, template_folder="templates")


@player_bp.route("/join_lobby", methods=["GET","POST"])
@login_required
def join_lobby():
    # Default page for player with a form to enter a lobby id
    if request.method == "POST":
        lobby_id = request.form.get("lobby_id")
        lobby = Lobby.query.filter(Lobby.id == lobby_id, Lobby.is_active == True).first()
        if lobby:
            # Check if user is already in lobby
            if current_user in lobby.users:
                return redirect(url_for("player.game"))
            # Add user to lobby
            lobby.users.append(current_user)
            db.session.commit()
            return redirect(url_for("player.game"))
        flash("Lobby does not exist")
    return render_template("game/index.html")


@player_bp.route("/game", methods=["GET"])
@login_required
def game():
    return render_template("game/game.html")


@player_bp.route("/leave_lobby", methods=["POST"])
@login_required
def leave_lobby():
    request_data = request.get_json()
    lobby_id = request_data.get("lobby_id")

    # Check if lobby exists
    lobby = Lobby.query.filter(Lobby.id == lobby_id, Lobby.is_active == True).first()

    if lobby:
        # Check if user is already in lobby
        if current_user not in lobby.users:
            return {"error": "User is not in lobby"}, 400

        # Remove user from lobby
        lobby.users.remove(current_user)
        lobby.save()
        return lobby.to_dict()

    return {"error": "Lobby does not exist"}, 400