# app/payments/forms.py
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class AddFundsForm(FlaskForm):
    amount = FloatField('Amount to Add ($)', 
                       validators=[DataRequired(), NumberRange(min=1, max=1000)])
    submit = SubmitField('Add Funds')

class CheckoutForm(FlaskForm):
    payment_method = SelectField('Payment Method', 
                                choices=[
                                    ('wallet', 'Wallet Balance'),
                                    ('credit_card', 'Credit Card (Simulated)'),
                                    ('mobile_money', 'Mobile Money (Simulated)')
                                ], 
                                validators=[DataRequired()])
    submit = SubmitField('Complete Purchase')

class RentalForm(FlaskForm):
    rental_days = SelectField('Rental Period',
                             choices=[
                                 (1, '1 Day'),
                                 (3, '3 Days'),
                                 (7, '7 Days'),
                                 (14, '14 Days'),
                                 (30, '30 Days')
                             ],
                             coerce=int,
                             validators=[DataRequired()])
    submit = SubmitField('Rent Book')