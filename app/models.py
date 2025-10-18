# app/models.py
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student')  # student, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    wallet = db.relationship('Wallet', backref='user', uselist=False, lazy=True, cascade='all, delete-orphan')
    books = db.relationship('Book', backref='uploader', lazy='dynamic', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic', foreign_keys='Transaction.user_id')
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Wallet(db.Model):
    __tablename__ = 'wallets'
    
    wallet_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def add_funds(self, amount):
        self.balance += amount
        return True
    
    def deduct_funds(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    def __repr__(self):
        return f'<Wallet {self.wallet_id} - User {self.user_id}>'

class Book(db.Model):
    __tablename__ = 'books'
    
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20))
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)  # Sale price
    rental_fee = db.Column(db.Float, default=0.0)  # Daily rental fee
    file_path = db.Column(db.String(500))
    status = db.Column(db.String(20), default='available')  # available, rented, sold
    category = db.Column(db.String(50))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='book', lazy='dynamic')
    
    def __repr__(self):
        return f'<Book {self.title}>'

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # purchase, rental
    status = db.Column(db.String(20), default='completed')  # completed, pending, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship for rental specialization
    rental = db.relationship('Rental', backref='transaction', uselist=False, lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Transaction {self.transaction_id} - {self.transaction_type}>'

class Rental(db.Model):
    __tablename__ = 'rentals'
    
    rental_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.transaction_id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(days=7))
    is_active = db.Column(db.Boolean, default=True)
    
    def calculate_due_date(self):
        return self.end_date
    
    def is_overdue(self):
        return datetime.utcnow() > self.end_date if self.is_active else False
    
    def __repr__(self):
        return f'<Rental {self.rental_id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))