from . import db

player_lobby_association = db.Table('player_lobby_association',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True),
    db.Column('lobby_id', db.Integer, db.ForeignKey('lobby.id'), primary_key=True)
)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    lobbies = db.relationship('Lobby', secondary=player_lobby_association, back_populates='players', lazy=True)
    scores = db.relationship('Score', backref='player', lazy=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lobbies": [lobby.to_dict() for lobby in self.lobbies],
            "scores": [score.to_dict() for score in self.scores]
        }