from flask_sqlalchemy import SQLAlchemy
from injector import inject
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user


class UserService:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def login(self, email, password):
        user = self.db.session.query(User).filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return True
        return False

    def signup(self, name, email, password):
        if self.db.session.query(User).filter_by(email=email).first():
            return None
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        self.db.session.add(new_user)
        self.db.session.commit()
        return new_user

    def get_user_by_email(self, email):
        return self.db.session.query(User).filter_by(email=email).first()
