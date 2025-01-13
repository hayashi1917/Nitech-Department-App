from flask import render_template, Blueprint
from models.model import Quiz 

select_bp = Blueprint('select', __name__)

@select_bp.route("/select")
def select():
    # データベースからクイズ一覧を取得 (idの昇順で表示)
    quizzes = Quiz.query.order_by(Quiz.id.asc()).all()
    
    return render_template("select.html", quizzes=quizzes)