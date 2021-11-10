from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/ok', methods=('GET', ))
def ok():
    return 'OK'
