from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash


app = create_app()

users_to_add = [
    ("admin", "admin123", "admin"),
    ("user", "user123", "user"),
]

with app.app_context():
    for username, password, role in users_to_add:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User '{username}' already exists — skipping.")
            continue

        hashed_pw = generate_password_hash(password)
        user = User(username=username, password_hash=hashed_pw, role=role)
        db.session.add(user)
        print(f"Added user: {username} with role: {role}")

    db.session.commit()
    print("✅ All users added successfully.")
