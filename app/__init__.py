# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# local import
from database.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])

    from routes.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    app.config.from_pyfile('../database/config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    return app
