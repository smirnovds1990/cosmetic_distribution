from flask import Blueprint, render_template
from flask_login import current_user
from werkzeug.exceptions import InternalServerError

from . import db


errorhandler_bp = Blueprint('error_handlers', __name__)


@errorhandler_bp.route('/cause_internal_error')
def cause_internal_error():
    """Маршрут для тестирования 500 ошибки."""
    raise InternalServerError('This is a test exception.')


@errorhandler_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', user=current_user), 404


@errorhandler_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
