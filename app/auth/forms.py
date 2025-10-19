# app/auth/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User

class RegistrationForm(FlaskForm):
    role = RadioField('Account Type', 
                     choices=[('student', 'Student'), ('admin', 'Administrator')],
                     default='student',
                     validators=[DataRequired()])
    
    student_id = StringField('Student ID', 
                            validators=[Optional()],
                            render_kw={"placeholder": "e.g., CUN2025100801"})
    
    admin_code = StringField('Admin Authorization Code',
                           validators=[Optional()],
                           render_kw={"placeholder": "Enter admin authorization code"})
    
    username = StringField('Username', 
                          validators=[DataRequired(), Length(min=2, max=20)],
                          render_kw={"placeholder": "Choose a unique username"})
    
    email = StringField('Email',
                       validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "your.email@university.edu"})
    
    password = PasswordField('Password', 
                            validators=[DataRequired()],
                            render_kw={"placeholder": "Create a strong password"})
    
    confirm_password = PasswordField('Confirm Password',
                                   validators=[DataRequired(), EqualTo('password')],
                                   render_kw={"placeholder": "Confirm your password"})
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_student_id(self, student_id):
        if self.role.data == 'student' and not student_id.data:
            raise ValidationError('Student ID is required for student accounts.')
        # Check if student ID already exists
        if student_id.data and self.role.data == 'student':
            existing_user = User.query.filter_by(student_id=student_id.data).first()
            if existing_user:
                raise ValidationError('This student ID is already registered.')

    def validate_admin_code(self, admin_code):
        if self.role.data == 'admin':
            if not admin_code.data:
                raise ValidationError('Admin authorization code is required.')
            # Change 'ADMIN_SECRET_123' to your actual admin code
            if admin_code.data != 'ADMIN_SECRET_123':
                raise ValidationError('Invalid admin authorization code.')

class LoginForm(FlaskForm):
    # Changed from 'email' to 'login_identifier' to accept both email and username
    login_identifier = StringField('Email or Username',
                                  validators=[DataRequired()],
                                  render_kw={"placeholder": "Enter your email or username"})
    
    password = PasswordField('Password', 
                            validators=[DataRequired()],
                            render_kw={"placeholder": "Enter your password"})
    
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')