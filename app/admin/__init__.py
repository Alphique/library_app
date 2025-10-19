# app/admin/__init__.py
from flask import Blueprint

bp = Blueprint('admin', __name__, template_folder='templates')  # This makes it look in app/admin/templates/

from app.admin import routes