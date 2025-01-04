from flask import Flask
from flask_migrate import Migrate
from model import db  # model.py から db をインポート
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")

    db_user = os.environ.get("DB_USER", "user")
    db_pass = os.environ.get("DB_PASS", "password")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "app_db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}'

    db.init_app(app)

    # Flask-Migrate の初期化
    migrate = Migrate(app, db)

    from controllers.index import index_bp
    from controllers.quiz import quiz_bp
    from controllers.result import result_bp
    from controllers.create import create_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(create_bp)
    
    return app