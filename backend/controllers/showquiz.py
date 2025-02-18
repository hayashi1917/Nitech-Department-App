from flask import Blueprint, render_template
from flask_login import current_user
from ..models.get import get_quizzes

showquiz_bp = Blueprint('showquiz', __name__, url_prefix='/showquiz')

@showquiz_bp.route("/")
#自分が作成したクイズの一覧を表示･削除
def showquiz():
    quizzes = get_quizzes(current_user.id)
    return render_template("showquiz.html", quizzes=quizzes)