# app/books/forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class BookForm(FlaskForm):
    title = StringField('Book Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=100)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=20)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
        ('textbook', 'Textbook'),
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('academic', 'Academic Paper'),
        ('research', 'Research Paper'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    price = FloatField('Sale Price ($)', validators=[Optional(), NumberRange(min=0)], default=0.0)
    rental_fee = FloatField('Rental Fee ($ per day)', validators=[Optional(), NumberRange(min=0)], default=0.0)
    book_file = FileField('Book File (PDF)', validators=[
        FileAllowed(['pdf'], 'PDF files only!')
    ])
    submit = SubmitField('Upload Book')

class SearchForm(FlaskForm):
    search = StringField('Search Books', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('textbook', 'Textbook'),
        ('fiction', 'Fiction'),
        ('non-fiction', 'Non-Fiction'),
        ('academic', 'Academic Paper'),
        ('research', 'Research Paper'),
        ('other', 'Other')
    ], validators=[Optional()])
    submit = SubmitField('Search')