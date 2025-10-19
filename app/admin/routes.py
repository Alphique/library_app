# app/admin/routes.py
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app.models import User, Book, Transaction, Wallet
from app.admin.forms import UserSearchForm, BookSearchForm, SystemSettingsForm, AnnouncementForm
from app import db
from app.admin import bp

@bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    # Statistics for dashboard
    total_users = User.query.count()
    total_books = Book.query.count()
    total_transactions = Transaction.query.count()
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',  # Use admin-specific template
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_books=total_books,
                         total_transactions=total_transactions,
                         recent_transactions=recent_transactions)

@bp.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    form = UserSearchForm()
    page = request.args.get('page', 1, type=int)
    
    # Build query based on form filters
    query = User.query
    
    if form.validate_on_submit() or request.args.get('username'):
        # Handle both form submission and pagination with filters
        username = form.username.data or request.args.get('username', '')
        email = form.email.data or request.args.get('email', '')
        role = form.role.data or request.args.get('role', '')
        status = form.status.data or request.args.get('status', '')
        
        if username:
            query = query.filter(User.username.contains(username))
        if email:
            query = query.filter(User.email.contains(email))
        if role:
            query = query.filter(User.role == role)
        if status:
            is_active = status == 'active'
            query = query.filter(User.is_active == is_active)
    
    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html', title='Manage Users', users=users, form=form)

@bp.route('/toggle_user/<int:user_id>')
@login_required
def toggle_user(user_id):
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = "activated" if user.is_active else "deactivated"
    flash(f'User {user.username} has been {status}.', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/make_admin/<int:user_id>')
@login_required
def make_admin(user_id):
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    user.role = 'admin'
    db.session.commit()
    
    flash(f'User {user.username} is now an administrator.', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    form = BookSearchForm()
    page = request.args.get('page', 1, type=int)
    
    # Build query based on form filters
    query = Book.query
    
    if form.validate_on_submit() or request.args.get('title'):
        # Handle both form submission and pagination with filters
        title = form.title.data or request.args.get('title', '')
        author = form.author.data or request.args.get('author', '')
        category = form.category.data or request.args.get('category', '')
        status = form.status.data or request.args.get('status', '')
        
        if title:
            query = query.filter(Book.title.contains(title))
        if author:
            query = query.filter(Book.author.contains(author))
        if category:
            query = query.filter(Book.category == category)
        if status:
            query = query.filter(Book.status == status)
    
    books = query.order_by(Book.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/books.html', title='Manage Books', books=books, form=form)

@bp.route('/delete_book/<int:book_id>')
@login_required
def delete_book(book_id):
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    
    flash(f'Book "{book.title}" has been deleted.', 'success')
    return redirect(url_for('admin.books'))

@bp.route('/transactions')
@login_required
def transactions():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/transactions.html', title='Transaction History', transactions=transactions)

@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    form = SystemSettingsForm()
    
    if form.validate_on_submit():
        # In a real app, you'd save these to a database table
        flash('System settings have been updated!', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html', title='System Settings', form=form)

@bp.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    if not current_user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('main.index'))
    
    form = AnnouncementForm()
    
    if form.validate_on_submit():
        # In a real app, you'd save announcements to a database
        flash('Announcement has been created!', 'success')
        return redirect(url_for('admin.announcements'))
    
    return render_template('admin/announcements.html', title='Manage Announcements', form=form)