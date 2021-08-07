from source import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    profile_pic = db.Column(db.String(20), nullable=False, default="default.jpg")

    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get_user_with_id(user_id):
        return User.query.filter_by(id=user_id).first()

    def create_user(self):
        db.session.add(self)
        db.session.commit()
