from flask import render_template, session, Blueprint, flash, redirect, url_for
import json
from ..gpt.gpt import get_GPT_response
from ..models.get import get_quiz

result_bp = Blueprint('result', __name__, url_prefix='/result')

@result_bp.route("/<quiz_id>")
def result(quiz_id):
    total_scores = session.get("total_scores", {})
    
    if not total_scores:
        flash("スコアデータが見つかりませんでした。")
        return redirect(url_for("select.select"))

    # スコアの最大値を取得
    max_score = max(info['score'] for info in total_scores.values())
    
    # 最高スコアの学科を取得
    best_departments = [
        info['department_name'] 
        for info in total_scores.values() 
        if info['score'] == max_score
    ]
    
    best_departments_str = json.dumps(best_departments, ensure_ascii=False)

    department_str = ""
    for info in total_scores.values():
        department_str += f"{info['department_name']}:{info['score']},"
    department_str = department_str.rstrip(',') 

    department_names_str = json.dumps(total_scores, ensure_ascii=False)

    quiz = get_quiz(quiz_id)
    university_name = quiz.university_name
    
    message = f"university_name: {university_name}, \n score: {department_str}"
    
    gpt_comment = get_GPT_response(message)

    return render_template(
        "result.html",
        departments=best_departments_str,
        department_str=department_str,
        department_names=department_names_str,
        gpt_comment=gpt_comment
    )