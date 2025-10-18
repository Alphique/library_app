# app/payments/__init__.py
from flask import Blueprint

bp = Blueprint('payments', __name__)

from app.payments import routes