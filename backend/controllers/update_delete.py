from flask import Blueprint, redirect, url_for
from ..models.delete import delete_quiz

update_delete_bp = Blueprint('update_delete', __name__)

@update_delete_bp.route("/delete/<quiz_id>")
#自分が作成したクイズの削除
def delete_myquiz(quiz_id):
    delete_quiz(quiz_id)
    return redirect(url_for("showquiz.showquiz"))