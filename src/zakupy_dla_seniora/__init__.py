from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from zakupy_dla_seniora.config import Config

mongo_db = MongoEngine()
sql_db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    mongo_db.init_app(app)
    sql_db.init_app(app)

    from zakupy_dla_seniora.main.routes import main
    app.register_blueprint(main)

    return app