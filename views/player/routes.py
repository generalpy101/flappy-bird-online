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
                return redirect(url_for("player.game", lobby_id=lobby_id))
            # Add user to lobby
            lobby.users.append(current_user)
            db.session.commit()
            return redirect(url_for("player.game", lobby_id=lobby_id))
        flash("Lobby does not exist", "error")
    return render_template("game/index.html")


@player_bp.route("/game", methods=["GET"])
@login_required
def game():
    lobby_id = request.args.get("lobby_id")
    
    if lobby_id is None:
        return redirect(url_for("player.join_lobby"))
    else:
        lobby_id = int(lobby_id)

    lobby = Lobby.query.filter(Lobby.id == lobby_id, Lobby.is_active == True).first()
    if not lobby:
        flash("Lobby does not exist", "error")
        return redirect(url_for("player.join_lobby"))
    
    if current_user not in lobby.users:
        flash("You are not in this lobby", "error")
        return redirect(url_for("player.join_lobby"))
    if len([score for score in current_user.scores if score.lobby_id == lobby_id]) >= 3:
        flash("You are only allowed to play 3 games per lobby", "info")
        return redirect(url_for("player.join_lobby"))
    
    # Get user's best score
    best_score = current_user.get_best_score(lobby_id=lobby_id)
    
    return render_template("game/game.html", lobby_id=lobby_id, best_score=best_score)


@player_bp.route("/player_able_to_play", methods=["GET"])
@login_required
def player_able_to_play():
    if len(current_user.scores) >= 3:
        return {"able_to_play": False}
    return {"able_to_play": True}


@player_bp.route("/submit_score", methods=["POST"])
@login_required
def submit_score():
    request_data = request.get_json()
    score = request_data.get("score")
    lobby_id = request_data.get("lobby_id")

    # Check if lobby exists
    lobby = Lobby.query.filter(Lobby.id == lobby_id, Lobby.is_active == True).first()

    if lobby:
        # Check if user is already in lobby
        if current_user not in lobby.users:
            return {"error": "User is not in lobby"}, 400
        
        lobby_id = int(lobby_id)

        # Check if user has already played 3 games
        if len([score for score in current_user.scores if score.lobby_id == lobby_id]) >= 3:
            return {"error": "User has already played 3 games"}, 400

        # Create score
        score = Score(score=score, player_id=current_user.id, lobby_id=lobby.id)
        db.session.add(score)
        db.session.commit()
        return score.to_dict()

    return {"error": "Lobby does not exist"}, 400


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