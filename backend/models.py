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
