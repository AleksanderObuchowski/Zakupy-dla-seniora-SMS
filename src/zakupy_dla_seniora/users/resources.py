from flask_restful import Resource, reqparse
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora import sql_db as db, bcrypt


register_parser = reqparse.RequestParser()
register_parser.add_argument('displayName', help='This field cannot be blank', required=True)
register_parser.add_argument('email', help='This field cannot be blank', required=True)
register_parser.add_argument('password', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = register_parser.parse_args()
        new_user = User(
            display_name=data['displayName'],
            email=data['email'],
            password=bcrypt.generate_password_hash(data['password'])
        )
        new_user.save()
        return {'success': True, 'message': 'Konto zostało stworzone.', 'id': new_user.id}, 200
