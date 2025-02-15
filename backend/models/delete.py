from ..models.model import Quiz, Department, Question, Option, Score, db

def delete_quiz(quiz_id):
    departments = Department.query.filter_by(quiz_id=quiz_id).all()
    for dept in departments:
        Score.query.filter_by(department_id=dept.id).delete()
    
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    for question in questions:
        Option.query.filter_by(question_id=question.id).delete()
    Question.query.filter_by(quiz_id=quiz_id).delete()
    
    Department.query.filter_by(quiz_id=quiz_id).delete()
    
    Quiz.query.filter_by(id=quiz_id).delete()
    
    db.session.commit()
