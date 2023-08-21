from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from models.lobby import Lobby
from models.user import User
from models import db

from views.auth.utils import admin_required

admin_bp = Blueprint("admin", __name__, template_folder="templates")


@admin_bp.route("/lobby", methods=["GET"])
@admin_required
def list_lobbies():
    lobbies = Lobby.query.all()
    return render_template("admin/index.html", lobbies=lobbies)


@admin_bp.route("/lobby/<int:lobby_id>", methods=["GET"])
@admin_required
def show_lobby(lobby_id):
    lobby = Lobby.query.filter(Lobby.id == lobby_id, Lobby.is_active == True).first()
    return render_template("admin/show.html", lobby=lobby)


@admin_bp.route("/lobby/create", methods=["POST"])
@admin_required
def create_lobby():
    request_data = request.get_json()
    name = request_data.get("name")
    if name:
        # Check lobby name is unique
        if Lobby.query.filter_by(name=name).first():
            return {"error": "Lobby name already exists"}, 400
        lobby = Lobby(name=name)
        db.session.add(lobby)
        db.session.commit()
        return lobby.to_dict()

    return {"error": "Name is required"}, 400


@admin_bp.route('/update_lobby_list', methods=['GET'])
def update_lobbies_list():
    result = []
    
    # Get the lobby object
    lobbies = Lobby.query.all()
    
    for lobby in lobbies:
        # Get the players in the lobby
        players = lobby.users
        
        # Create a dictionary of the lobby's data
        lobby_data = {
            'id': lobby.id,
            'name': lobby.name,
            'players_count': len(players),
            'is_active': lobby.is_active
        }
        
        # Add the lobby's data to the lobby list
        result.append(lobby_data)

    # Return the updated lobby list data as JSON
    return jsonify(result)


@admin_bp.route('/update_player_list', methods=['GET'])
def update_players_list():
    args = request.args
    lobby_id = args.get('lobby_id')
    
    result = []
    
    # Get the lobby object
    lobby = Lobby.query.filter(Lobby.id == lobby_id, Lobby.is_active == True).first()
    
    # Get the players in the lobby
    players = lobby.users
    
    for player in players:
        # Create a dictionary of the player's data
        score = player.calculate_average_score(lobby_id=lobby_id)
        best_score = player.get_best_score(lobby_id=lobby_id)
        player_data = {
            'id': player.id,
            'username': player.name,
            'score': score,
            'best_score': best_score
        }
        
        # Add the player's data to the player list
        result.append(player_data)

    # Return the updated player list data as JSON
    return jsonify(result)