from . import db
from . import bcrypt
from flask_login.mixins import UserMixin

player_lobby_association = db.Table(
    "player_lobby_association",
    db.Column("player_id", db.Integer, db.ForeignKey("player.id"), primary_key=True),
    db.Column("lobby_id", db.Integer, db.ForeignKey("lobby.id"), primary_key=True),
)


class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    reg_id = db.Column(db.String(255), nullable=False)
    lobbies = db.relationship(
        "Lobby", secondary=player_lobby_association, back_populates="players", lazy=True
    )
    scores = db.relationship("Score", backref="user", lazy=True)
    
    def get_best_score(self, lobby_id):
        if not self.scores:
            return 0
        
        lobby_id = int(lobby_id)

        lobby_scores = [score.score for score in self.scores if score.lobby_id == lobby_id]
        
        try:
            best_score = max(lobby_scores)
        except Exception as e:
            print(e)
            best_score = 0
        return best_score
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "reg_id": self.reg_id,
            "lobbies": [lobby.to_dict() for lobby in self.lobbies],
            "scores": [score.to_dict() for score in self.scores],
        }
