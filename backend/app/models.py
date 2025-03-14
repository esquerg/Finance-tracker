from . import db 
from enum import Enum

class TransactionType(Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

#Define the models which will create the DB tables 
class Account(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime, default = db.func.current_timestamp())

    def get_balance(self):
        income = db.session.query(db.func.sum(Transaction.amount)).filter_by(account_id=self.id, type=TransactionType.INCOME).scalar() or 0
        expense = db.session.query(db.func.sum(Transaction.amount)).filter_by(account_id=self.id, type=TransactionType.EXPENSE).scalar() or 0
        return income - expense

    def __repr__(self):
        return f'<Account {self.name} - {self.get_balance()}>'
    
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    type = db.Column(db.Enum(TransactionType), nullable=False)  # Reference to Enum here
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())

    account = db.relationship('Account', backref=db.backref('transactions', lazy=True))
    category = db.relationship('Category', backref=db.backref('transactions', lazy=True))

    def __repr__(self):
        return f'<Transaction {self.type} - {self.amount}>'
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Category {self.name}>'