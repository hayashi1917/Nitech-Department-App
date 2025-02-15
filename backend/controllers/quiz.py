from flask import (Blueprint, redirect, render_template, request,
                session, url_for)
from flask_login import login_required
from ..models.get import get_departments, get_options, get_questions, get_scores, get_quizzes, get_quiz

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz_bp.route("/<int:quiz_id>/<int:question_id>", methods=["GET", "POST"])
@login_required
def quiz(quiz_id, question_id):
    # quiz_id に基づいて質問一覧を取得
    quiz = get_quiz(quiz_id)
    questions = get_questions(quiz_id)
    departments = get_departments(quiz_id)
    options = get_options(questions[question_id - 1].id)
    option_ids = [o.id for o in options]
    print("option_ids:",option_ids)
    total_score = {}
    print("questions:",questions)
    
    # セッションを初期化
    if "total_scores" not in session or not session["total_scores"]:
        session["total_scores"] = {}
        for department in departments:
            session["total_scores"][str(department.id)] = {
                "score": 0,
                "department_name": department.department_name
            }
        session.modified = True

    
    # デバッグ用のログ出力を追加
    print("Session total_scores:", session["total_scores"])
    print("Departments:", [(d.id, type(d.id)) for d in departments])

    # GET: 指定された問題を表示
    if request.method == "GET":
        current_question = questions[question_id - 1]
        current_options = get_options(current_question.id)
        print("current_options:", current_options)
        return render_template(
            "quiz.html",
            quiz=quiz,
            question=current_question,
            question_id=question_id,
            total_questions=len(questions),
            options=current_options,
            option_ids=option_ids
        )

    if request.method == "POST":
        selected_option = request.form.get("option")
        print("selected_option:",selected_option)
        if selected_option is None:
            error = "選択肢を選んでください。"
            return render_template(
                "quiz.html",
                question=questions[question_id - 1],
                question_id=question_id,
                total_questions=len(questions),
                error=error
            )
        #ここで現時点の学部ごとのスコアを計算しておく
        for department in departments:
            score = get_scores(options[int(selected_option)].id, department.id)
            print("department.id:",department.id)
            print("options[int(selected_option)].id:",options[int(selected_option)].id)
            print("score:",score.score)
            session["total_scores"][str(department.id)]["score"] += score.score
            session.modified = True
        print("session total_scores:", session["total_scores"])
        if question_id >= len(questions):
            return redirect(url_for("result.result", quiz_id=quiz_id))
        else:
            return redirect(url_for("quiz.quiz", quiz_id=quiz_id, question_id=question_id + 1))

@quiz_bp.route("/clear_session")    
def clear_session():
    session.clear()
    session.modified = True 
    print("Session cleared")
    return redirect(url_for("select.select"))