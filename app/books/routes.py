# app/books/routes.py
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from app.books.forms import BookForm, SearchForm
from app.models import Book, User
from app import db
from app.books import bp

@bp.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    search_form = SearchForm()
    
    # Build query based on search parameters
    query = Book.query.filter_by(status='available')
    
    search = request.args.get('search')
    category = request.args.get('category')
    
    if search:
        query = query.filter(Book.title.contains(search) | Book.author.contains(search))
    if category:
        query = query.filter_by(category=category)
    
    books = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('books/catalog.html', 
                         title='Book Catalog', 
                         books=books, 
                         search_form=search_form)

@bp.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('books/book_detail.html', title=book.title, book=book)

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # Prevent admins from uploading books
    if current_user.is_admin():
        flash('Admins cannot upload books. Please use the admin panel to manage books.', 'warning')
        return redirect(url_for('admin.books'))
    
    form = BookForm()
    if form.validate_on_submit():
        # Handle file upload
        if form.book_file.data:
            filename = secure_filename(form.book_file.data.filename)
            # Store files in static/uploads/books/
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'books')
            os.makedirs(upload_folder, exist_ok=True)  # Create directory if it doesn't exist
            file_path = os.path.join(upload_folder, filename)
            form.book_file.data.save(file_path)
            
            # Store relative path for web access
            relative_path = f"uploads/books/{filename}"
        else:
            relative_path = None
        
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            description=form.description.data,
            category=form.category.data,
            price=form.price.data,
            rental_fee=form.rental_fee.data,
            file_path=relative_path,  # Store relative path
            uploaded_by=current_user.user_id
        )
        
        db.session.add(book)
        db.session.commit()
        
        flash('Your book has been uploaded!', 'success')
        return redirect(url_for('books.catalog'))
    
    return render_template('books/upload.html', title='Upload Book', form=form)


@bp.route('/my-books')
@login_required
def my_books():
    page = request.args.get('page', 1, type=int)
    books = Book.query.filter_by(uploaded_by=current_user.user_id)\
                     .paginate(page=page, per_page=12, error_out=False)
    return render_template('books/my_books.html', title='My Books', books=books)

@bp.route('/delete/<int:book_id>')
@login_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Check if user owns the book
    if book.uploaded_by != current_user.user_id and not current_user.is_admin():
        flash('You can only delete your own books.', 'danger')
        return redirect(url_for('books.my_books'))
    
    # Delete file if exists
    if book.file_path and os.path.exists(book.file_path):
        os.remove(book.file_path)
    
    db.session.delete(book)
    db.session.commit()
    
    flash('Book has been deleted.', 'success')
    return redirect(url_for('books.my_books'))

# Add this debug route
@bp.route('/debug-book-file/<int:book_id>')
def debug_book_file(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Build the expected URL
    expected_url = url_for('static', filename='uploads/books/' + book.file_path, _external=True) if book.file_path else None
    
    return f"""
    <h3>Book File Debug</h3>
    <strong>Book:</strong> {book.title} (ID: {book.book_id})<br>
    <strong>File path in database:</strong> {book.file_path}<br>
    <strong>Expected URL:</strong> {expected_url}<br>
    <strong>Test Link:</strong> <a href="{expected_url}" target="_blank">{expected_url}</a><br>
    <br>
    <strong>Manual Test URLs:</strong><br>
    <a href="/static/uploads/books/{book.file_path}" target="_blank">/static/uploads/books/{book.file_path}</a>
    """