from flask import Blueprint

bp = Blueprint("demo_blueprint", __name__, url_prefix='/')


@bp.route('/')
def index():
    return "lalala"
