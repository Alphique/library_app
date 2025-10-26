# app/payments/routes.py
from flask import render_template, url_for, flash, redirect, request, session
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from app.payments.forms import AddFundsForm, CheckoutForm, RentalForm
from app.models import Book, Transaction, Rental, Wallet
from app import db
from app.payments import bp

# app/payments/routes.py - Update wallet function
@bp.route('/wallet', methods=['GET', 'POST'])
@login_required
def wallet():
    # Prevent admins from accessing wallet
    if current_user.is_admin():
        flash('Admins do not have wallets. Please use the admin dashboard.', 'warning')
        return redirect(url_for('admin.dashboard'))
    
    form = AddFundsForm()
    
    # Calculate total earnings from user's uploaded books
    total_earnings = db.session.query(db.func.sum(Transaction.amount)).filter(
        Transaction.book_id.in_(
            db.session.query(Book.book_id).filter_by(uploaded_by=current_user.user_id)
        )
    ).scalar() or 0.0
    
    if form.validate_on_submit():
        # Add funds to wallet
        current_user.wallet.add_funds(form.amount.data)
        db.session.commit()
        flash(f'${form.amount.data:.2f} has been added to your wallet!', 'success')
        return redirect(url_for('payments.wallet'))
    
    return render_template('payments/wallet.html', 
                         title='My Wallet', 
                         form=form,
                         total_earnings=total_earnings)  # Add this variable


@bp.route('/add-to-cart/<int:book_id>')
@login_required
def add_to_cart(book_id):
    # Prevent admins from using cart
    if current_user.is_admin():
        flash('Admins cannot purchase or rent books.', 'warning')
        return redirect(url_for('books.book_detail', book_id=book_id))
    
    book = Book.query.get_or_404(book_id)
    
    # Initialize cart in session if not exists
    if 'cart' not in session:
        session['cart'] = []
    
    # Check if book is already in cart
    cart_item = {
        'book_id': book.book_id,
        'title': book.title,
        'author': book.author,
        'price': book.price,
        'rental_fee': book.rental_fee,
        'type': 'purchase'  # default to purchase
    }
    
    # Add to cart if not already there
    if not any(item['book_id'] == book_id for item in session['cart']):
        session['cart'].append(cart_item)
        session.modified = True
        flash(f'"{book.title}" has been added to your cart!', 'success')
    else:
        flash(f'"{book.title}" is already in your cart!', 'info')
    
    return redirect(url_for('books.book_detail', book_id=book_id))

@bp.route('/cart')
@login_required
def cart():
    # Prevent admins from accessing cart
    if current_user.is_admin():
        flash('Admins cannot purchase or rent books.', 'warning')
        return redirect(url_for('admin.dashboard'))
    
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items if item['type'] == 'purchase')
    return render_template('payments/cart.html', title='Shopping Cart', cart_items=cart_items, total=total)

@bp.route('/remove-from-cart/<int:book_id>')
@login_required
def remove_from_cart(book_id):
    # Prevent admins from using cart
    if current_user.is_admin():
        flash('Admins cannot purchase or rent books.', 'warning')
        return redirect(url_for('admin.dashboard'))
    
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['book_id'] != book_id]
        session.modified = True
        flash('Item removed from cart!', 'success')
    
    return redirect(url_for('payments.cart'))

@bp.route('/rent/<int:book_id>', methods=['GET', 'POST'])
@login_required
def rent_book(book_id):
    # Prevent admins from renting books
    if current_user.is_admin():
        flash('Admins cannot rent books.', 'warning')
        return redirect(url_for('books.book_detail', book_id=book_id))
    
    book = Book.query.get_or_404(book_id)
    form = RentalForm()
    
    if form.validate_on_submit():
        rental_days = form.rental_days.data
        total_cost = book.rental_fee * rental_days
        
        # Check if user has enough balance
        if current_user.wallet.balance < total_cost:
            flash('Insufficient funds in your wallet!', 'danger')
            return redirect(url_for('payments.wallet'))
        
        # Create transaction
        transaction = Transaction(
            user_id=current_user.user_id,
            book_id=book.book_id,
            amount=total_cost,
            transaction_type='rental',
            status='completed'
        )
        db.session.add(transaction)
        db.session.commit()
        
        # Create rental record
        rental = Rental(
            transaction_id=transaction.transaction_id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=rental_days)
        )
        db.session.add(rental)
        
        # Deduct from user's wallet and add to book owner's wallet
        current_user.wallet.deduct_funds(total_cost)
        book_owner_wallet = Wallet.query.filter_by(user_id=book.uploaded_by).first()
        book_owner_wallet.add_funds(total_cost)
        
        # Update book status
        book.status = 'rented'
        
        db.session.commit()
        
        flash(f'Book rented successfully for {rental_days} days!', 'success')
        return redirect(url_for('payments.transaction_history'))
    
    return render_template('payments/rent.html', title='Rent Book', book=book, form=form)

@bp.route('/purchase/<int:book_id>')
@login_required
def purchase_book(book_id):
    # Prevent admins from purchasing books
    if current_user.is_admin():
        flash('Admins cannot purchase books.', 'warning')
        return redirect(url_for('books.book_detail', book_id=book_id))
    
    book = Book.query.get_or_404(book_id)
    
    # Check if user has enough balance
    if current_user.wallet.balance < book.price:
        flash('Insufficient funds in your wallet!', 'danger')
        return redirect(url_for('payments.wallet'))
    
    # Create transaction
    transaction = Transaction(
        user_id=current_user.user_id,
        book_id=book.book_id,
        amount=book.price,
        transaction_type='purchase',
        status='completed'
    )
    db.session.add(transaction)
    
    # Deduct from user's wallet and add to book owner's wallet
    current_user.wallet.deduct_funds(book.price)
    book_owner_wallet = Wallet.query.filter_by(user_id=book.uploaded_by).first()
    book_owner_wallet.add_funds(book.price)
    
    # Update book status
    book.status = 'sold'
    book.uploaded_by = current_user.user_id  # Transfer ownership
    
    db.session.commit()
    
    flash('Book purchased successfully!', 'success')
    return redirect(url_for('payments.transaction_history'))

@bp.route('/transaction-history')
@login_required
def transaction_history():
    # Admins see all transactions, students see only their own
    if current_user.is_admin():
        transactions = Transaction.query.order_by(Transaction.created_at.desc()).all()
    else:
        transactions = Transaction.query.filter_by(user_id=current_user.user_id)\
                                      .order_by(Transaction.created_at.desc())\
                                      .all()
    
    # Calculate statistics for the template
    total_spent = sum(t.amount for t in transactions if t.amount > 0)
    purchase_count = sum(1 for t in transactions if t.transaction_type == 'purchase')
    rental_count = sum(1 for t in transactions if t.transaction_type == 'rental')
    
    return render_template('payments/transaction_history.html', 
                         title='Transaction History', 
                         transactions=transactions,
                         total_spent=total_spent,
                         purchase_count=purchase_count,
                         rental_count=rental_count)