from flask import (Blueprint,flash, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_required
from ..models.create import create_quiz
from ..models.model import db
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

create_bp = Blueprint('create', __name__)

@create_bp.route('/step1', methods=['GET', 'POST'])
@login_required
def step1():
    """
    クイズ作成の最初のステップ - クイズの基本情報の入力
    
    Returns:
        GET: クイズ作成フォーム
        POST: 次のステップへのリダイレクト
    """
    
    print("Current session at start of step1:", session.get('data'))
    
    if 'data' not in session:
        session['data'] = {}
    
    if request.method == 'POST':
        try:
            form_data = {
                "university_name": request.form['university_name'],
                "department_count": int(request.form['department_count']),
                "question_count": int(request.form['question_count']),
                "option_count": int(request.form['option_count']),
                "created_by": current_user.id
            }
            
            session['data']['quiz'] = form_data
            session.modified = True
            
            print("データ入力後のセッション:", session.get('data'))
            
            return redirect(url_for('create.step2'))
            
        except (KeyError, ValueError) as e:
            print(f"Error in step1: {str(e)}")
            flash('入力データが不正です。', 'error')
            return redirect(url_for('create.step1'))
    
    return render_template("step1.html")

@create_bp.route('/step2', methods=['GET', 'POST'])
@login_required
def step2():
    """
    クイズ作成の第二ステップ - 学部の入力
    
    Returns:
        GET: 学部入力フォーム
        POST: 次のステップへのリダイレクト
    """
    
    if request.method == 'POST':
        departments = request.form.getlist('departments[]')
        session['data']['departments'] = departments
        session.modified = True
        return redirect(url_for('create.step3'))
    return render_template("step2.html",
                            department_count=session['data']['quiz']['department_count']
                        )

@create_bp.route('/step3', methods=['GET', 'POST'])
@login_required
def step3():
    """
    クイズ作成の第三ステップ - 質問の入力
    
    Returns:
        GET: 質問入力フォーム
        POST: 次のステップへのリダイレクト
    """
    
    if request.method == 'POST':
        questions = request.form.getlist('questions[]')
        session['data']['questions'] = questions
        session.modified = True
        return redirect(url_for('create.step4'))
    return render_template("step3.html",
                            question_count=session['data']['quiz']['question_count']
                        )

@create_bp.route('/step4', methods=['GET', 'POST'])
@login_required
def step4():
    """
    クイズ作成の最終ステップ - スコアの設定と保存
    
    Returns:
        GET: スコア入力フォーム
        POST: クイズ保存後のリダイレクト
    """

    try:
        if request.method == 'POST':
            logger.debug("Received form data:", request.form)
            
            # 2次元配列として初期化
            session['data']['scores'] = []
            question_count = session['data']['quiz']['question_count']
            option_count = session['data']['quiz']['option_count']
            department_count = session['data']['quiz']['department_count']
            
            # 質問ごとのループ
            for q_idx in range(question_count):
                question_scores = []
                
                # 選択肢ごとのループ
                for o_idx in range(option_count):
                    try:
                        option_text = request.form.getlist(f'options[{q_idx}][]')[o_idx]
                            
                        option_data = {
                            "option": option_text,
                            "scores": []
                        }
                        
                        # 学部ごとのスコア
                        for d_idx in range(department_count):
                            score_str = request.form.getlist(f'scores[{q_idx}][{o_idx}][]')[d_idx]
                            score = int(score_str)
                        
                                
                            option_data["scores"].append({
                                "department": session['data']['departments'][d_idx],
                                "score": score
                            })
                            
                        question_scores.append(option_data)
                        
                    except (IndexError, ValueError) as e:
                        flash(str(e), 'error')
                        return redirect(url_for('create.step4'))
                
                session['data']['scores'].append({
                    "question": session['data']['questions'][q_idx],
                    "options": question_scores
                })
            
            session.modified = True
            
            # データベースに保存
            try:
                quiz = create_quiz(session['data'])
                db.session.commit()
                flash('クイズが正常に作成されました。', 'success')
                
                # セッションをクリア
                session.pop('data', None)
                session.modified = True
                
                return redirect(url_for('index.index'))
                
            except (SQLAlchemyError, ValueError) as e:
                db.session.rollback() 
                flash(f'クイズの保存に失敗しました: {str(e)}', 'error')
                return redirect(url_for('create.step4'))
        
        return render_template(
            'step4.html',
            questions=session['data']['questions'],
            departments=session['data']['departments'],
            question_count=session['data']['quiz']['question_count'],
            option_count=session['data']['quiz']['option_count']
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in step4: {str(e)}")
        flash('予期せぬエラーが発生しました。', 'error')
        return redirect(url_for('create.step1'))