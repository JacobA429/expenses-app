from backend import db
from sqlalchemy import ForeignKey

from backend.models import User


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