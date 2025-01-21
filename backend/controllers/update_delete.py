from flask import render_template, Blueprint, redirect, request
from ..models.get import get_quizzes
update_delete_bp = Blueprint('update_delete', __name__)

#@update_delete_bp.route("/update_delete")
#def update_delete():
#    curret_user.username = get_current_user
#    quiz = get_quiz(quiz_id)
#    return render_template("update-delete.html",user_mailaddress="test@test.com",quiz_title="test_quiz")

