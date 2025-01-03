import os
from flask import render_template, session, Blueprint
import json
from gpt.gpt import get_GPT_response

result_bp = Blueprint('result', __name__, url_prefix='/result')

current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(current_dir)

questions_path = os.path.join(base_dir, 'data', 'questions.json')
departments_path = os.path.join(base_dir, 'data', 'departments.json')

with open(questions_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

with open(departments_path, "r", encoding="utf-8") as f:
    departments = json.load(f)

@result_bp.route("/")
def result():
    responses = session.get("responses", [])
    department_scores = {dept: 0 for dept in departments.keys()}
    print(f"Responses: {responses}")

    for i, selected_option_index in enumerate(responses):
        option = questions[i]["options"][selected_option_index]
        for dept, points in option["score"].items():
            department_scores[dept] += points

    max_score = max(department_scores.values())

    best_departments = [
        dept for dept, score in department_scores.items() if score == max_score
    ]

    gpt_comment = get_GPT_response(
        EM=department_scores["EM"],
        PE=department_scores["PE"],
        LC=department_scores["LC"],
        AC=department_scores["AC"],
        CS=department_scores["CS"],
    )

    department_scores_str = ""
    for dept, score in department_scores.items():
        department_scores_str += dept + ":" + str(score) + ","

    return render_template(
        "result.html",
        departments=best_departments,
        department_str=department_scores_str,
        department_names=departments,
        gpt_comment=gpt_comment,
    )