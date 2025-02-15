from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from .models.model import db, User 

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY")

    db_user = os.environ.get("DB_USER", "user")
    db_pass = os.environ.get("DB_PASS", "password")
    db_host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "app_db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}'

    db.init_app(app)
    login_manager = LoginManager()
    #アプリをログイン機能を紐付ける
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_view = 'login.login'  # Blueprintのエンドポイントに修正

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Flask-Migrate の初期化
    migrate = Migrate(app, db)

    from .controllers.index import index_bp
    from .controllers.quiz import quiz_bp
    from .controllers.result import result_bp
    from .controllers.create import create_bp
    from .controllers.select import select_bp
    from .controllers.login import login_bp
    from .controllers.update_delete import update_delete_bp
    from .controllers.showquiz import showquiz_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(create_bp)
    app.register_blueprint(select_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(update_delete_bp)
    app.register_blueprint(showquiz_bp)
    return app