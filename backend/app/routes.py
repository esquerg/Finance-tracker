from flask import Blueprint, request, jsonify
from . import db
from .models import Account, Transaction, Category, TransactionType
from sqlalchemy.exc import SQLAlchemyError

# Create a Blueprint for routes
bp = Blueprint('/api', __name__)

@bp.route('/accounts', methods=['GET'])
def get_accounts():
    try:
        accounts = Account.query.all()
        #Creating a list of dictionaris with 'account_name' and 'balance'
        accounts_data = [{'id': account.id, 'name': account.name, 'balance': str(account.get_balance()), 'created_at': account.created_at} for account in accounts]
        return jsonify(accounts_data), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error':'Could not retrieve accounts'}), 500
    
@bp.route('/accounts/<int:id>', methods=['GET'])
def get_account(id=None):
    try:
        account = Account.query.get(id)

        if not account:
            return jsonify({'error': 'Account not found'}), 404
    
        return jsonify({'id': account.id, 'name': account.name, 'balance': str(account.get_balance()), 'created_at': account.created_at}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error':'Could not retrieve accounts'}), 500
    
@bp.route('/accounts', methods=['POST'])
def add_account():
    try:
        data = request.get_json()
        print(data)
        new_account = Account(name=data['name'])
        db.session.add(new_account)
        db.session.commit()
        return jsonify({'message':'Account created successfully.'}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error':'Could not create account.'}), 500

#Transaction Routes
#Get all Transactions for all Accounts
@bp.route('/transactions', methods=['GET'])
def get_transactions():
    try:
        transactions = Transaction.query.all()
        print(transactions)
        #Creating a list of dictionaries with transaction
        transactions_data = [{'id':transaction.id,'account_id': transaction.account_id, 'type': transaction.type.value, 'amount': transaction.amount, 'category_id': transaction.category_id, 'description': transaction.description, 'date': transaction.date} for transaction in transactions]
        return jsonify(transactions_data), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error':'Could not retrieve transactions'}), 500

#Get all transactions for a single account
@bp.route('/transactions/<int:id>', methods=['GET'])
def get_transactions_for_account(id):
    try:
        transactions = Transaction.query.filter_by(account_id=id)
        transactions_data = [{'id': transaction.id, 'account_id': transaction.account_id, 'type': transaction.type.value, 'amount': transaction.amount, 'category_id': transaction.category_id, 'description': transaction.description, 'date': transaction.date} for transaction in transactions]
        return jsonify(transactions_data),201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error':'Could not retrieve transaction'}), 500
    
@bp.route('/transactions', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        new_transaction = Transaction(account_id=data['account_id'], type=data['type'], amount=data['amount'], 
                                      category_id=data['category_id'], description=data['description'])
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({'message':'Transaction created successfully'}),201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error':'Could not create transaction'}), 500
    
@bp.route('/transactions/<int:id>', methods=['POST'])
def update_transaction(id):
    try:
        # Fetch the transaction
        transaction = Transaction.query.get(id)
        if not transaction:
            return jsonify({'error': 'The transaction cannot be found.'}), 404

        data = request.get_json()

        # Check if account_id is being changed
        new_account_id = data.get('account_id')
        if new_account_id is not None and new_account_id != transaction.account_id:
            new_account = Account.query.get(new_account_id)
            if not new_account:
                return jsonify({'error': 'Invalid account ID.'}), 400
            transaction.account_id = new_account_id

        # Update type if provided
        new_type = data.get('type')
        if new_type:
            try:
                transaction.type = TransactionType[new_type.upper()]
            except KeyError:
                return jsonify({'error': 'Invalid transaction type.'}), 400

        # Update amount if provided
        if 'amount' in data:
            transaction.amount = data['amount']

        # Update category if provided
        if 'category_id' in data:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({'error': 'Invalid category ID.'}), 400
            transaction.category_id = data['category_id']

        # Update description if provided
        if 'description' in data:
            transaction.description = data['description']

        db.session.commit()
        return jsonify({'message': 'Transaction updated successfully'}), 201

    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error': 'Could not update transaction'}), 500
    
@bp.route('/categories', methods=['GET'])
def get_categorys():
    try:
        categories_data = Category.query.all()
        categories = [{'name': category.name, 'created_at': category.created_at} for category in categories_data]
        return jsonify(categories), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error':'Could not retrieve categories'}), 500
    
@bp.route('/categories', methods=['POST'])
def add_category():
    try:
        data = request.get_json()
        new_category = Category(name=data['name'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify({'message':'Category created successfully.'}), 201
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'error':'Could not create category'}), 500