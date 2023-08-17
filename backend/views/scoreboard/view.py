from flask import Blueprint, jsonify, request

from models import db
from models.score import Score

scoreboard_bp = Blueprint("scoreboard", __name__, url_prefix="/scoreboard")

@scoreboard_bp.route("", methods=["GET"])
def get_scores():
    query_params = request.args
    lobby_id = query_params.get("lobby_id")
    if lobby_id:
        scores = Score.query.filter_by(lobby_id=lobby_id)
    else:
        scores = Score.query.all()
    scores_response = []
    for score in scores:
        scores_response.append(score.to_dict())
    return jsonify(scores_response), 200


@scoreboard_bp.route("/create", methods=["POST"], strict_slashes=False)
def create_score():
    request_body = request.get_json()
    score = request_body.get("score")
    lobby_id = request_body.get("lobby_id")
    player_id = request_body.get("player_id")
    if not score:
        return jsonify({"error": "Invalid score"}), 400
    new_score = Score(
            score=score,
            lobby_id=lobby_id,
            player_id=player_id
        )
    db.session.add(new_score)
    db.session.commit()
    return jsonify(new_score.to_dict()), 201