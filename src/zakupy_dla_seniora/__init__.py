from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from zakupy_dla_seniora.config import Config

mongo_db = MongoEngine()
sql_db = SQLAlchemy()


def register_blueprints(app):
    from zakupy_dla_seniora.main.routes import main
    app.register_blueprint(main)


def register_api_resources(api):
    from zakupy_dla_seniora.main.resources import Main
    api.add_resource(Main, '/main_api')


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)
    api = Api(app)

    register_blueprints(app)
    register_api_resources(api)

    mongo_db.init_app(app)
    sql_db.init_app(app)

    return app