# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Book, Transaction, Wallet, User
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/dashboard')
@login_required
def dashboard():
    # If admin tries to access student dashboard, redirect to admin dashboard
    if current_user.role == 'admin':  # Direct role check
        print(f"Admin user {current_user.username} accessed student dashboard, redirecting...")
        return redirect(url_for('admin.dashboard'))
    
    # Get student-specific data for the dashboard
    user_books = Book.query.filter_by(uploaded_by=current_user.user_id).all()
    user_transactions = Transaction.query.filter_by(user_id=current_user.user_id).order_by(Transaction.created_at.desc()).limit(10).all()
    
    # Ensure wallet exists and get it
    wallet = current_user.wallet
    if not wallet:
        wallet = Wallet(user_id=current_user.user_id, balance=0.00)
        db.session.add(wallet)
        db.session.commit()
        # Refresh to get the wallet without reassigning current_user
        wallet = Wallet.query.filter_by(user_id=current_user.user_id).first()
    
    return render_template('dashboard.html', 
                         title='Student Dashboard',
                         user_books=user_books,
                         user_transactions=user_transactions,
                         wallet=wallet)

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile')