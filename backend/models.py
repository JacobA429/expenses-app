# backend/models.py
import bcrypt
from werkzeug.security import generate_password_hash

from backend import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }


class Couple(db.Model):
    __tablename__ = 'couples'

    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer)
    user2_id = db.Column(db.Integer)


    def __init__(self, user1_id, user2_id):
        self.user1_id = user1_id
        self.user2_id = user2_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @property
    def user1(self) -> User:
        return User.query.filter_by(id=self.user1_id).first()

    @property
    def user2(self) -> User:
        return User.query.filter_by(id=self.user2_id).first()

    def json(self):
        return {
            'id': self.id,
            'user1': self.user1.json(),
            'user2_id': self.user2.json(),
        }
