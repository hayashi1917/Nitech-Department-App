from flask import Flask, render_template, request, redirect, url_for, session
import json
from gpt.gpt import get_GPT_response


app = Flask(__name__)
app.secret_key = "your_secret_key"  # セキュアなキーに置き換えてください

# 質問と学科のデータを読み込み
with open("data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

with open("data/departments.json", "r", encoding="utf-8") as f:
    departments = json.load(f)


@app.route("/")
def index():
    session["responses"] = []
    return render_template("index.html")


@app.route("/quiz/<int:question_id>", methods=["GET", "POST"])
def quiz(question_id):
    if "responses" not in session:
        session["responses"] = []

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
            return redirect(url_for("result"))
        else:
            return redirect(url_for("quiz", question_id=question_id + 1))

    question = questions[question_id - 1]
    return render_template(
        "quiz.html",
        question=question,
        question_id=question_id,
        total_questions=len(questions),
    )

@app.route("/result-test")
def result_test():
    return render_template(
        "result.html",
        departments=[],
        department_str="EM:1,PE:2,LC:3,AC:4,CS:5,",
        department_names=departments,
        gpt_comment="このページは、テストページとなりますので結果は適切なものではありません。このページが表示された場合は速やかに閉じて初めからやり直してくださいまた、再度やり直してもこのページが表示される場合は、開発者への連絡をお願いします。連絡先->0X0-XXXX-XXXX.YYY-ZZZ@exsample.info",
    )

@app.route("/result")
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

    print(gpt_comment)

    # debug

    # print(responses)
    # print(department_scores)
    # print(best_departments)
    
    department_scores_str = ""
    for dept, score in department_scores.items():
        department_scores_str += dept + ":" + str(score) + ","
    # print(department_scores_str)

    return render_template(
        "result.html",
        departments=best_departments,
        department_str=department_scores_str,
        department_names=departments,
        gpt_comment=gpt_comment,
    )

if __name__ == "__main__":
    app.run(debug=True)
