# backend/models.py
import bcrypt
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash

from backend import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    couple_id = db.Column(db.Integer, db.ForeignKey('couples.id'))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password, method='sha256')

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def join_couple(self, couple_id):
        self.couple_id = couple_id
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }


class Couple(db.Model):
    __tablename__ = 'couples'

    id = db.Column(db.Integer, primary_key=True)
    expenses = db.relationship("Expense", backref="couple", lazy="dynamic")
    users = db.relationship('User', backref='couple')

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def json(self):
        return {
            'id': self.id,
            'user1': self.users[0].json(),
            'user2': self.users[1].json()
        }


class Expense(db.Model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45))
    total = db.Column(db.Float)
    created_at = db.Column(db.Date)
    couple_id = db.Column(db.Integer, db.ForeignKey('couples.id'), nullable=False)
    paid_by_user_id = db.Column(db.Integer, ForeignKey('users.id'))

    def __init__(self, title, total, created_at, paid_by_user_id, couple_id):
        self.total = total
        self.paid_by_user_id = paid_by_user_id
        self.created_at = created_at
        self.couple_id = couple_id
        self.title = title

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def paid_for_by_user(self) -> User:
        return User.query.filter_by(id=self.paid_by_user_id).first()

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'total': self.total,
            'created_at': self.created_at,
            'paid_for_by_user': self.paid_for_by_user().json()
        }
