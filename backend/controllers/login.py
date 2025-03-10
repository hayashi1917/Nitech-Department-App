from flask import (Blueprint, redirect, render_template, request, url_for)
from flask_login import current_user, logout_user
from ..models.user import user_login, user_signup

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route("/", methods=['GET', 'POST'])
#ログイン画面を表示
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))
        
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        results = user_login(username, password)
        if results:
            return redirect(url_for("index.index"))
        return render_template("login.html", error="メールアドレスまたはパスワードが間違っています")
        
    return render_template("login.html")

@login_bp.route("/logout")
#ログアウト
def logout():
    logout_user()
    return redirect(url_for("login.login"))

@login_bp.route("/signup", methods=['GET', 'POST'])
#新規登録画面を表示
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index.index"))
        
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        results = user_signup(username, password)
        if results:
            return redirect(url_for("login.login"))
        return render_template("signup.html", error="このユーザー名は既に使用されています")
        
    return render_template("signup.html")

