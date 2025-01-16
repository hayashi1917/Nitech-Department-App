from flask import (Blueprint, flash, redirect, render_template, request,
                session, url_for)
from flask_login import current_user, login_required
from models.get import get_departments, get_options, get_questions, get_scores, get_quizzes, get_quiz

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')

@quiz_bp.route("/<int:quiz_id>/<int:question_id>", methods=["GET", "POST"])
@login_required
def quiz(quiz_id, question_id):
    # quiz_id に基づいて質問一覧を取得
    quiz = get_quiz(quiz_id)
    questions = get_questions(quiz_id)
    departments = get_departments(quiz_id)
    options = get_options(question_id)
    question_ids = [q.id for q in questions]
    department_ids = [d.id for d in departments]
    option_ids = [o.id for o in options]
    
    
    # セッションを初期化
    if "total_scores" not in session or not session["total_scores"]:
        session["total_scores"] = {}
        for department in departments:
            # department.id は整数
            session["total_scores"][department.id] = 0
        session.modified = True

    
    # デバッグ用のログ出力を追加
    print("Session total_scores:", session["total_scores"])
    print("Departments:", [(d.id, type(d.id)) for d in departments])

    # GET: 指定された問題を表示
    if request.method == "GET":
        return render_template(
            "quiz.html",
            quiz=quiz,
            questions=questions,
            question_ids=question_ids,
            options=options,
            option_ids=option_ids
        )

    if request.method == "POST":
        selected_option = request.form.get("option")
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
            session["total_scores"][department.id] += score.score
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