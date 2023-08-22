import os

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user

from models.player import Player
from models.lobby import Lobby
from models.score import Score
from models import db

player_bp = Blueprint("player", __name__, template_folder="templates")

LIVES = os.getenv("LIVES") or 10


@player_bp.route("/join_lobby", methods=["GET", "POST"])
def join_lobby():
    # Default page for player with a form to enter a lobby id
    if request.method == "POST":
        lobby_id = request.form.get("lobby_id")
        reg_id = request.form.get("reg_id")
        username = request.form.get("username")

        lobby = Lobby.query.filter(
            Lobby.id == lobby_id, Lobby.is_active == True
        ).first()
        if lobby:
            # Check if player exists, if not create player
            player = Player.query.filter(Player.reg_id == reg_id).first()
            if not player:
                player = Player(reg_id=reg_id, username=username)
                db.session.add(player)
                db.session.commit()

            if player in lobby.players:
                return redirect(
                    url_for("player.game", lobby_id=lobby_id, player_id=player.id)
                )
            # Add user to lobby
            lobby.players.append(player)
            db.session.commit()
            return redirect(
                url_for("player.game", lobby_id=lobby_id, player_id=player.id)
            )
        flash("Lobby does not exist", "error")
    return render_template("game/index.html")


@player_bp.route("/game", methods=["GET"])
def game():
    lobby_id = request.args.get("lobby_id")
    player_id = request.args.get("player_id")

    if lobby_id is None:
        return redirect(url_for("player.join_lobby"))
    else:
        lobby_id = int(lobby_id)

    if player_id is None:
        return redirect(url_for("player.join_lobby"))
    else:
        player_id = int(player_id)

    player = Player.query.filter(Player.id == player_id).first()
    lobby = Lobby.query.filter(Lobby.id == lobby_id, Lobby.is_active == True).first()
    if not lobby:
        flash("Lobby does not exist", "error")
        return redirect(url_for("player.join_lobby"))

    if player not in lobby.players:
        flash("You are not in this lobby", "error")
        return redirect(url_for("player.join_lobby"))

    if len([score for score in player.scores if score.lobby_id == lobby_id]) >= LIVES:
        flash(f"You are only allowed to play {LIVES} games per lobby", "info")
        return redirect(url_for("player.join_lobby"))

    # Get user's best score
    best_score = player.get_best_score(lobby_id=lobby_id)

    return render_template(
        "game/game.html", lobby_id=lobby_id, best_score=best_score, player_id=player_id
    )


@player_bp.route("/player_able_to_play", methods=["GET"])
def player_able_to_play():
    if len(current_user.scores) >= 3:
        return {"able_to_play": False}
    return {"able_to_play": True}


@player_bp.route("/submit_score", methods=["POST"])
def submit_score():
    request_data = request.get_json()
    score = request_data.get("score")
    lobby_id = request_data.get("lobby_id")
    player_id = request_data.get("player_id")

    # Check if lobby exists
    lobby = Lobby.query.filter(Lobby.id == lobby_id, Lobby.is_active == True).first()
    player = Player.query.filter(Player.id == player_id).first()

    if lobby:
        # Check if user is already in lobby
        if player not in lobby.players:
            return {"error": "User is not in lobby"}, 400

        lobby_id = int(lobby_id)
        player_id = int(player_id)

        if (
            len([score for score in player.scores if score.lobby_id == lobby_id])
            >= LIVES
        ):
            flash(f"You are only allowed to play {LIVES} games per lobby", "info")
            return {"error": f"User has already played {LIVES} games"}, 400

        # Create score
        score = Score(score=score, player_id=player_id, lobby_id=lobby.id)
        db.session.add(score)
        db.session.commit()
        return score.to_dict()

    return {"error": "Lobby does not exist"}, 400
