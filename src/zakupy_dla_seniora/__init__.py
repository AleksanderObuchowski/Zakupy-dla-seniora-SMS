from flask import Flask
from zakupy_dla_seniora.config import Config

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

    from zakupy_dla_seniora.main.routes import main
    app.register_blueprint(main)

    return app