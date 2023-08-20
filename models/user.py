from . import db
from . import bcrypt
from flask_login.mixins import UserMixin

user_lobby_association = db.Table(
    "user_lobby_association",
    db.Column("player_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("lobby_id", db.Integer, db.ForeignKey("lobby.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    _password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    lobbies = db.relationship(
        "Lobby", secondary=user_lobby_association, back_populates="users", lazy=True
    )
    scores = db.relationship("Score", backref="user", lazy=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        if self._password is not None:
            self._password = bcrypt.generate_password_hash(self._password).decode(
                "utf-8"
            )

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext_password):
        self._password = bcrypt.generate_password_hash(plaintext_password).decode(
            "utf-8"
        )

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password, plaintext_password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lobbies": [lobby.to_dict() for lobby in self.lobbies],
            "scores": [score.to_dict() for score in self.scores],
        }
