from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from settings import Config


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()


def create_app(config_class=None):
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object(Config)
    db.init_app(app)
    from . import views
    app.register_blueprint(views.main_bp)
    from . import error_handlers
    app.register_blueprint(error_handlers.errorhandler_bp)
    from .error_handlers import page_not_found
    app.register_error_handler(404, page_not_found)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    with app.app_context():
        from . import (
            constants, error_handlers, forms, models, validators, views
        )
    return app
