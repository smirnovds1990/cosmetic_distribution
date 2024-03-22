from flask import render_template
from flask_login import current_user

from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', user=current_user), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
