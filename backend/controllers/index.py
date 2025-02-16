from flask import render_template, session, Blueprint

index_bp = Blueprint('index', __name__)

@index_bp.route("/")
def index():
    session["total_scores"] = {}
    session.modified = True
    return render_template("index.html")
