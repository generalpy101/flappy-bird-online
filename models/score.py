from . import db


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lobby_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    is_best = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "player_id": self.player_id,
            "lobby_id": self.lobby_id,
            "score": self.score,
            "is_best": self.is_best,
        }
