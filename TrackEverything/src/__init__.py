from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import app_config
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import traceback
from src.common.messages import NOT_HAVE_PERMITIONS_MESSAGE
from src.common.validation import LOGGING_DATE_FORMAT
from src.services.password_validator.password_validator import PasswordValidator


db = MongoEngine()
login_manager = LoginManager()
password_validator = PasswordValidator()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=3)
    logger = logging.getLogger('tdm')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    Bootstrap(app)
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = NOT_HAVE_PERMITIONS_MESSAGE
    login_manager.login_view = "auth.login"

    from .core.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .core import core as core_blueprint
    app.register_blueprint(core_blueprint)

    from .core.projects import project as project_blueprint
    app.register_blueprint(project_blueprint)

    from .core.users import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .core.tasks import task as task_blueprint
    app.register_blueprint(task_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    @app.after_request
    def after_request(response):
        timestamp = strftime(LOGGING_DATE_FORMAT)
        logger.info('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme,
                    request.full_path, response.status)

        return response

    @app.errorhandler(Exception)
    def exceptions(error):
        timestamp = strftime(LOGGING_DATE_FORMAT)
        trace = traceback.format_exc()
        logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s', timestamp, request.remote_addr, request.method,
                     request.scheme, request.full_path, trace)
        return internal_server_error(error)

    password_validator.teach()

    return app
