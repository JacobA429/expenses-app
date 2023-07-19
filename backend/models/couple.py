from backend import db


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
        json_expenses = []
        for expense in self.expenses:
            json_expenses.append(expense.json())
        return {
            'id': self.id,
            'user1': self.users[0].json(),
            'user2': self.users[1].json(),
            'expenses': json_expenses
        }
