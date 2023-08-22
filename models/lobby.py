from . import db

from .player import player_lobby_association


class Lobby(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    players = db.relationship(
        "Player",
        secondary=player_lobby_association,
        back_populates="lobbies",
        lazy=True,
    )
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "players": [player.to_dict() for player in self.players],
            "is_active": self.is_active,
        }
