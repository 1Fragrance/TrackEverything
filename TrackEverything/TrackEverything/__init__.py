from flask import Flask
from config import app_config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager

db = MongoEngine()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    return app


