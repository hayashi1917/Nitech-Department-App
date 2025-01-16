from models.model import User, Quiz, Department, Question, Option, Score

def get_user(id):
    return User.query.filter_by(id=id).first()

def get_quizzes(user_id):
    return Quiz.query.filter_by(created_by=user_id).all()

def get_quiz(quiz_id):
    return Quiz.query.filter_by(id=quiz_id).first()

def get_departments(quiz_id):
    return Department.query.filter_by(quiz_id=quiz_id).all()

def get_questions(quiz_id):
    return Question.query.filter_by(quiz_id=quiz_id).all()

def get_options(question_id):
    return Option.query.filter_by(question_id=question_id).all()

def get_scores(option_id, department_id):
    return Score.query.filter_by(option_id=option_id, department_id=department_id).first()