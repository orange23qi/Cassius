from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    db.app = app

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .mysql import mysql as mysql_blueprint
    app.register_blueprint(mysql_blueprint, url_prefix='/mysql')

    from .redis import redis as redis_blueprint
    app.register_blueprint(redis_blueprint, url_prefix='/redis')

    from .workflow import workflow as workflow_blueprint
    app.register_blueprint(workflow_blueprint, url_prefix='/workflow')

    from .workflow.mysql import workflow_mysql as workflow_mysql_blueprint
    app.register_blueprint(workflow_mysql_blueprint, url_prefix='/workflow/mysql')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
