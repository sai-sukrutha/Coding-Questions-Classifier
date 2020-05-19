from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(120), index=False, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Questions(db.Model):
    Qid = db.Column(db.Integer, primary_key=True)
    Qname = db.Column(db.String(50), nullable=False)
    Ques_link = db.Column(db.String(100), nullable=False)
    Sol_link = db.Column(db.String(100))
    Platform = db.Column(db.String(10), nullable=False)


class QuestionTags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Tag = db.Column(db.String(20), nullable=False)
    Ques_id = db.Column(db.Integer, nullable=False)      #Qid of Questions


db.create_all()


