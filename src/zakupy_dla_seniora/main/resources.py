from flask_restful import Resource, reqparse


main_parser = reqparse.RequestParser()
main_parser.add_argument('name', help='This field cannot be blank.', required=True, type=str)


class Main(Resource):
    def post(self):
        name = main_parser.parse_args()['name']
        return {'success': True, 'method_type': 'post', 'message': f'Hello, {name}'}, 200

    def get(self):
        return {'success': True, 'method_type': 'get', 'message': 'Hello World'}, 200