from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key_123")
    
    from controllers.index import index_bp
    from controllers.quiz import quiz_bp
    from controllers.result import result_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(result_bp)

    return app