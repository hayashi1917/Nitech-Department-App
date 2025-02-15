from flask import Blueprint, render_template
from flask_login import current_user
from ..models.get import get_quizzes

showquiz_bp = Blueprint('showquiz', __name__, url_prefix='/showquiz')

@showquiz_bp.route("/")
def showquiz():
    quizzes = get_quizzes(current_user.id)
    return render_template("showquiz.html", quizzes=quizzes)