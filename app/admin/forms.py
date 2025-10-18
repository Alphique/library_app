# app/admin/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Optional, Email, NumberRange

class UserSearchForm(FlaskForm):
    username = StringField('Username', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    role = SelectField('Role', choices=[
        ('', 'All Roles'),
        ('student', 'Student'),
        ('admin', 'Admin')
    ], validators=[Optional()])
    status = SelectField('Status', choices=[
        ('', 'All Status'),
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], validators=[Optional()])
    submit = SubmitField('Search Users')

class BookSearchForm(FlaskForm):
    title = StringField('Title', validators=[Optional()])
    author = StringField('Author', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('textbook', 'Textbook'),
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('academic', 'Academic Paper'),
        ('research', 'Research Paper'),
        ('other', 'Other')
    ], validators=[Optional()])
    status = SelectField('Status', choices=[
        ('', 'All Status'),
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('sold', 'Sold')
    ], validators=[Optional()])
    submit = SubmitField('Search Books')

class SystemSettingsForm(FlaskForm):
    site_name = StringField('Site Name', validators=[DataRequired()], default='CUZ Library')
    default_rental_days = IntegerField('Default Rental Days', 
                                      validators=[DataRequired(), NumberRange(min=1, max=365)], 
                                      default=7)
    transaction_fee = FloatField('Transaction Fee (%)', 
                                validators=[DataRequired(), NumberRange(min=0, max=50)], 
                                default=0.0)
    max_file_size = IntegerField('Max File Size (MB)', 
                                validators=[DataRequired(), NumberRange(min=1, max=100)], 
                                default=16)
    site_description = TextAreaField('Site Description', validators=[Optional()])
    submit = SubmitField('Save Settings')

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    is_active = SelectField('Status', choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], validators=[DataRequired()])
    submit = SubmitField('Create Announcement')