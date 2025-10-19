import os
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect

# --- Ensure correct working directory ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- Initialize Flask app and DB context ---
app = create_app()
app.app_context().push()

# --- Account details ---
username = "admin"
password = "admin123"
student_id = "CUN2025100801"
full_name = "Testing1@"

# --- Check model columns dynamically ---
inspector = inspect(db.engine)
columns = [col["name"] for col in inspector.get_columns("user")]  # adjust "user" if table is named differently

# --- Build user attributes safely ---
user_data = {
    "username": username,
    "password_hash": generate_password_hash(password),
    "full_name": full_name
}

if "student_id" in columns:
    user_data["student_id"] = student_id

# --- Check if user exists ---
existing_user = User.query.filter_by(username=username).first()
if existing_user:
    print(f"⚠️ User '{username}' already exists.")
else:
    new_user = User(**user_data)
    db.session.add(new_user)
    db.session.commit()
    print(f"✅ User '{username}' created successfully.")

# --- Optional: show summary ---
print("\n📘 Created User Info:")
for k, v in user_data.items():
    print(f"{k}: {v}")
