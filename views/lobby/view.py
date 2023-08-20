from flask import Blueprint, jsonify, request

from models.lobby import Lobby
from models import db

lobby_bp = Blueprint("lobby", __name__, url_prefix="/lobbies")

@lobby_bp.route("", methods=["GET"])
def get_lobbies():
    filters = {}
    args = request.args
    lobby_id = args.get("lobby_id")
    is_active = True if args.get("is_active") == "true" else False
    name = args.get("name")
        
    if is_active:
        filters["is_active"] = is_active
    if lobby_id:
        filters["id"] = lobby_id
    if name:
        filters["name"] = name
    
    if filters:
        lobbies = Lobby.query.filter_by(**filters)
    else:
        lobbies = Lobby.query.all()
    lobbies_response = []
    for lobby in lobbies:
        lobbies_response.append(lobby.to_dict())
    return jsonify(lobbies_response), 200


@lobby_bp.route("/create", methods=["POST"], strict_slashes=False)
def create_lobby():
    request_body = request.get_json()
    lobby_name = request_body.get("name")
    if not lobby_name:
        return jsonify({"error": "Invalid lobby name"}), 400
    # Check if lobby name already exists
    existing_lobby = Lobby.query.filter_by(name=lobby_name).first()
    if existing_lobby:
        return jsonify({"error": "Lobby name already exists"}), 400
    new_lobby = Lobby(name=request_body["name"])
    db.session.add(new_lobby)
    db.session.commit()
    return jsonify(new_lobby.to_dict()), 201


@lobby_bp.route("/set_inactive", methods=["POST"], strict_slashes=False)
def set_lobby_inactive():
    request_body = request.get_json()
    lobby_id = request_body.get("lobby_id")
    if not lobby_id:
        return jsonify({"error": "Invalid lobby"}), 400
    lobby = Lobby.query.get(lobby_id)
    if not lobby:
        return jsonify({"error": "Invalid lobby"}), 400
    lobby.is_active = False
    db.session.commit()
    return jsonify({"success": f"Lobby {lobby_id} set to inactive"}), 201


@lobby_bp.route("/set_active", methods=["POST"], strict_slashes=False)
def set_lobby_active():
    request_body = request.get_json()
    lobby_id = request_body.get("lobby_id")
    if not lobby_id:
        return jsonify({"error": "Invalid lobby"}), 400
    lobby = Lobby.query.get(lobby_id)
    if not lobby:
        return jsonify({"error": "Invalid lobby"}), 400
    lobby.is_active = True
    db.session.commit()
    return jsonify({"success": f"Lobby {lobby_id} set to active"}), 201