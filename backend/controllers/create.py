import datetime

from flask import (Blueprint, current_app, flash, jsonify, redirect,
                   render_template, request, session, url_for)
from flask_login import current_user, login_required
from ..models.create import create_quiz
from ..models.model import Department, Option, Question, Quiz, Score, db
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

create_bp = Blueprint('create', __name__)

@create_bp.route('/step1', methods=['GET', 'POST'])
@login_required
def step1():
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
            
            print("Session after saving quiz data:", session.get('data'))
            
            return redirect(url_for('create.step2'))
            
        except (KeyError, ValueError) as e:
            print(f"Error in step1: {str(e)}")
            flash('入力データが不正です。', 'error')
            return redirect(url_for('create.step1'))
    
    return render_template("step1.html")

@create_bp.route('/step2', methods=['GET', 'POST'])
@login_required
def step2():
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
    if not _validate_quiz_session():
        flash('最初のステップから入力してください。', 'warning')
        return redirect(url_for('create.step1'))

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
        
        # GETリクエスト時のレンダリング
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

def _validate_quiz_session():
    """クイズセッションデータの検証"""
    try:
        if 'data' not in session:
            return False
        if 'quiz' not in session['data']:
            return False
            
        required_fields = [
            'university_name', 
            'department_count', 
            'question_count', 
            'option_count', 
            'created_by'
        ]
        
        return all(
            field in session['data']['quiz'] 
            for field in required_fields
        )
    except Exception:
        return False

def _get_current_step():
    """現在のステップを判定"""
    if 'data' not in session:
        return 1
    data = session['data']
    if 'quiz' not in data:
        return 1
    if 'departments' not in data:
        return 2
    if 'questions' not in data:
        return 3
    return 4

def _get_missing_fields():
    """必要なフィールドの欠落をチェック"""
    required_fields = {
        'quiz': ['university_name', 'department_count', 
                'question_count', 'option_count', 'created_by'],
        'departments': [],
        'questions': []
    }
    
    missing = {}
    data = session.get('data', {})
    
    for section, fields in required_fields.items():
        if section not in data:
            missing[section] = 'section_missing'
        elif fields:
            missing[section] = [
                field for field in fields 
                if field not in data[section]
            ]
            
    return missing

@create_bp.route('/debug/session', methods=['GET'])
@login_required
def debug_session():
    """開発環境でセッションの状態を確認するためのエンドポイント"""
    if not current_app.debug:
        return jsonify({'error': 'Debug endpoint is disabled in production'}), 403
        
    debug_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'session_data': {
            'data': session.get('data'),
            'session_keys': list(session.keys()),
        },
        'session_status': {
            'has_data': 'data' in session,
            'has_quiz': 'quiz' in session.get('data', {}),
            'current_step': _get_current_step(),
        },
        'quiz_data': session.get('data', {}).get('quiz', {}),
        'validation': {
            'is_valid': _validate_quiz_session(),
            'missing_fields': _get_missing_fields()
        }
    }
    
    return jsonify(debug_data)
