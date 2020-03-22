from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from zakupy_dla_seniora.config import Config


sql_db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'


def register_blueprints(app):
    from zakupy_dla_seniora.main.routes import main
    app.register_blueprint(main)


def register_api_resources(api):
    from zakupy_dla_seniora.users.resources import UserRegistration
    api.add_resource(UserRegistration, '/register')

    from zakupy_dla_seniora.sms_code_verification.resources import SendSMSCode, CheckSMSCode
    api.add_resource(SendSMSCode, '/send_code')
    api.add_resource(CheckSMSCode, '/check_code')

    from zakupy_dla_seniora.sms_handler.resources import ReceiveSMS
    api.add_resource(ReceiveSMS, '/sms')

    from zakupy_dla_seniora.board_view.resources import BoardView
    api.add_resource(BoardView, '/board')

    from zakupy_dla_seniora.profile_view.resources import ProfileView
    api.add_resource(ProfileView, '/profile')

    from zakupy_dla_seniora.placings.resources import PlacingCreation
    api.add_resource(PlacingCreation, '/placing')

    from zakupy_dla_seniora.leaderboards.resources import Leaderboards
    api.add_resource(Leaderboards, '/leaderboards')

    from zakupy_dla_seniora.placings.resources import PlacingEnding
    api.add_resource(PlacingEnding, '/end_placing')


def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)
    api = Api(app)

    register_blueprints(app)
    register_api_resources(api)

    sql_db.init_app(app)
    login_manager.init_app(app)

    return app
