import logging
from .model import Department, Option, Question, Quiz, Score, db
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

def create_quiz(data):
    """クイズデータをデータベースに保存する

    Args:
        data (dict): セッションに保存されたクイズデータ

    Returns:
        Quiz: 作成されたクイズオブジェクト
        
    Raises:
        SQLAlchemyError: データベース操作でエラーが発生した場合
    """
    try:
        # クイズの作成
        quiz = Quiz(
            university_name=data['quiz']['university_name'],
            department_count=data['quiz']['department_count'],
            question_count=data['quiz']['question_count'],
            option_count=data['quiz']['option_count'],
            created_by=data['quiz']['created_by']
        )
        db.session.add(quiz)
        db.session.flush()  # IDを取得するためにフラッシュ
        
        # 学部の作成とIDの保持
        departments = {}
        for department_name in data['departments']:
            department = Department(
                department_name=department_name,
                quiz_id=quiz.id
            )
            db.session.add(department)
            departments[department_name] = department
        db.session.flush()
        
        # 質問、選択肢、スコアの作成
        for question_data in data['scores']:
            question = Question(
                question_text=question_data['question'],
                quiz_id=quiz.id
            )
            db.session.add(question)
            db.session.flush()
            
            for option_data in question_data['options']:
                option = Option(
                    option_text=option_data['option'],
                    question_id=question.id
                )
                db.session.add(option)
                db.session.flush()
                
                for score_data in option_data['scores']:
                    score = Score(
                        score=score_data['score'],
                        option_id=option.id,
                        department_id=departments[score_data['department']].id
                    )
                    db.session.add(score)
        
        db.session.flush()  # 全ての変更をフラッシュ
        return quiz
            
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise     