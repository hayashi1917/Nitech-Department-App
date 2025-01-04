from flask import render_template, session, Blueprint

create_bp = Blueprint('create', __name__)

@create_bp.route("/create")
def create():
    return render_template("create.html")