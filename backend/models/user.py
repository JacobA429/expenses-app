from backend import db
from werkzeug.security import generate_password_hash


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