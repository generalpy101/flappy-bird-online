from flask import Blueprint, jsonify, request

from models.player import Player
from models.lobby import Lobby
from models import db

player_bp = Blueprint("player", __name__, url_prefix="/players")

@player_bp.route("", methods=["GET"])
def get_players():
    args = request.args
    player_id = args.get("player_id")
    if player_id:
        players = Player.query.filter_by(id=player_id)
    else:
        players = Player.query.all()
        
    players_response = []
    for player in players:
        players_response.append(player.to_dict())
    return jsonify(players_response), 200

@player_bp.route("/create", methods=["POST"], strict_slashes=False)
def create_player():
    request_body = request.get_json()
    player_name = request_body.get("name")
    if not player_name:
        return jsonify({"error": "Invalid player name"}), 400
    # Check if player name already exists
    existing_player = Player.query.filter_by(name=player_name).first()
    if existing_player:
        return jsonify({"error": "Player name already exists"}), 400
    new_player = Player(name=request_body["name"])
    db.session.add(new_player)
    db.session.commit()
    return jsonify(new_player.to_dict()), 201


@player_bp.route("/add_to_lobby", methods=["POST"], strict_slashes=False)
def add_player_to_lobby():
    request_body = request.get_json()
    player_id = request_body.get("player_id")
    lobby_id = request_body.get("lobby_id")
    if not player_id or not lobby_id:
        return jsonify({"error": "Invalid player or lobby"}), 400
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Invalid player"}), 400
    lobby = Lobby.query.get(lobby_id)
    if not lobby:
        return jsonify({"error": "Invalid lobby"}), 400
    lobby.players.append(player)
    db.session.commit()
    return jsonify({"success": f"Player {player_id} added to lobby {lobby_id}"}), 201


@player_bp.route("/remove_from_lobby", methods=["POST"], strict_slashes=False)
def remove_player_from_lobby():
    request_body = request.get_json()
    player_id = request_body.get("player_id")
    lobby_id = request_body.get("lobby_id")
    if not player_id or not lobby_id:
        return jsonify({"error": "Invalid player or lobby"}), 400
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Invalid player"}), 400
    lobby = Lobby.query.get(lobby_id)
    if not lobby:
        return jsonify({"error": "Invalid lobby"}), 400
    lobby.players.remove(player)
    db.session.commit()
    return jsonify({"success": f"Player {player_id} removed from lobby {lobby_id}"}), 201


@player_bp.route("/<player_id>/lobbies", methods=["GET"])
def get_lobbies_for_player(player_id):
    player = Player.query.get(player_id)
    if not player:
        return jsonify({"error": "Invalid player"}), 400
    lobbies = player.lobbies
    lobbies_response = []
    for lobby in lobbies:
        lobbies_response.append(lobby.to_dict())
    return jsonify(lobbies_response), 200


@player_bp.route("/lobby_players", methods=["GET"])
def get_players_for_lobby():
    args = request.args
    lobby_id = args.get("lobby_id")
    if not lobby_id:
        return jsonify({"error": "Invalid lobby"}), 400
    lobby = Lobby.query.get(lobby_id)
    if not lobby:
        return jsonify({"error": "Invalid lobby"}), 400
    players = lobby.players
    players_response = []
    for player in players:
        players_response.append(player.to_dict())
    return jsonify(players_response), 200