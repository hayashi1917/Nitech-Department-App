from flask import render_template, request, redirect, url_for, session, Blueprint
import json, os

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')

current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(os.path.dirname(current_dir), 'data', 'questions.json')

with open(json_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

@quiz_bp.route("/<int:question_id>", methods=["GET", "POST"])
def quiz(question_id):
    print(question_id)
    if "responses" not in session:
        session["responses"] = []
    
    # GETメソッドの処理追加
    if request.method == "GET":
        return render_template(
            "quiz.html",
            question=questions[question_id - 1],
            question_id=question_id,
            total_questions=len(questions)
        )

    if request.method == "POST":
        selected_option = request.form.get("option")
        print(selected_option)
        if selected_option is None:
            error = "選択肢を選んでください。"
            return render_template(
                "quiz.html", question=questions[question_id - 1], error=error
            )

        responses = session.get("responses")
        responses.append(int(selected_option))
        session["responses"] = responses

        if question_id >= len(questions):
            return redirect(url_for("result.result"))
        else:
            return redirect(url_for("quiz.quiz", question_id=question_id + 1))