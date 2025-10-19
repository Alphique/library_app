# app/auth/routes.py
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app.auth.forms import RegistrationForm, LoginForm
from app.models import User, Wallet
from app import db, bcrypt
from app.auth import bp

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
        if existing_user:
            flash('Email or username already exists!', 'danger')
            return render_template('register.html', title='Register', form=form)
        
        # Create user based on role
        user = User(
            username=form.username.data, 
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        # Set student_id if it's a student account
        if form.role.data == 'student':
            # Check if student_id already exists
            existing_student = User.query.filter_by(student_id=form.student_id.data).first()
            if existing_student:
                flash('This student ID is already registered!', 'danger')
                return render_template('register.html', title='Register', form=form)
            user.student_id = form.student_id.data
        
        db.session.add(user)
        db.session.flush()  # This assigns user_id without committing
        
        # Create wallet for user with initial balance (only for students)
        if form.role.data == 'student':
            wallet = Wallet(user_id=user.user_id, balance=100.00)
            db.session.add(wallet)
        
        db.session.commit()
        
        if form.role.data == 'student':
            flash(f'Your student account has been created with $100 welcome bonus! You can now log in.', 'success')
        else:
            flash('Your administrator account has been created! You can now log in.', 'success')
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # If already logged in, redirect based on role - FIXED
        print(f"Already authenticated: {current_user.username}, Role: {current_user.role}, is_admin: {current_user.is_admin()}")
        if current_user.role == 'admin':  # Use direct role check for safety
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        login_identifier = form.login_identifier.data
        password = form.password.data
        
        # Try to find user by email OR username OR student_id
        user = User.query.filter(
            (User.email == login_identifier) | 
            (User.username == login_identifier) |
            (User.student_id == login_identifier)
        ).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact administrator.', 'danger')
                return render_template('login.html', title='Login', form=form)
            
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            
            # Ensure wallet exists for students (backward compatibility)
            if user.role == 'student' and not user.wallet:
                wallet = Wallet(user_id=user.user_id, balance=0.00)
                db.session.add(wallet)
                db.session.commit()
            
            # DEBUG: Print user info for troubleshooting
            print(f"LOGIN SUCCESS: User: {user.username}, Role: {user.role}, is_admin(): {user.is_admin()}")
            
            # Role-based redirect after login - FIXED with direct role check
            if user.role == 'admin':
                flash(f'Welcome back, Administrator {user.username}!', 'success')
                # Force redirect to admin dashboard, ignore next_page for admins
                return redirect(url_for('admin.dashboard'))
            else:
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check your credentials and try again.', 'danger')
    
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))