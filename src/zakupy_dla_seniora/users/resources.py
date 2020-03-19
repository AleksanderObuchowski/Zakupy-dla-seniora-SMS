from flask_restful import Resource, reqparse
from zakupy_dla_seniora.users.models import User


register_parser = reqparse.RequestParser()
register_parser.add_argument('name', help='This field cannot be blank', required=True)
register_parser.add_argument('password', help='This field cannot be blank', required=True)
register_parser.add_argument('first_name', help='This field cannot be blank', required=True)
register_parser.add_argument('last_name', help='This field cannot be blank', required=True)
register_parser.add_argument('phone', help='This field cannot be blank', required=True)


class UserRegistration(Resource):
    def post(self):
        data = register_parser.parse_args()
        new_user = User(
            name=data['name'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],
            phone=data['phone'].replace(' ', '+')
        )
        new_user.save()
        return {'success': True, 'message': 'Konto zostało stworzone.', 'id': new_user.id}, 200

