from flask_login import logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from .model import db, User

def user_login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.hashed_password, password):
        login_user(user)
        return True
    else:
        return False

def user_signup(username, password):
    # 既存のユーザーがあるかチェック
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return False  # 既に存在するのでFalseを返す

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return True

def user_logout():
    logout_user()
