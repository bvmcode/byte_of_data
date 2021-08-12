from source import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user = User.get_user_with_id(user_id)
    print('XXXXXXXXXXXXXXXXXX', user_id)
    if user:
        print(user.name, flush=True)
    return user

class User(db.Model, UserMixin):
    id_pk = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    profile_pic = db.Column(db.String(200), nullable=False, default="default.jpg")

    def __init__(self, id, name, email, profile_pic):
        self.id = id
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get_user_with_id(user_id):
        return User.query.filter_by(id=user_id).first()

    def create_user(self):
        db.session.add(self)
        db.session.commit()
