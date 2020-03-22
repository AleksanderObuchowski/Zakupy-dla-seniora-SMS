from flask_restful import Resource, reqparse
from twilio.rest import Client
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token, twilio_phone


client = Client(twilio_sid, twilio_auth_token)

sending_parser = reqparse.RequestParser()
sending_parser.add_argument('user_id', help='This field cannot be blank.', required=True, type=str)
sending_parser.add_argument('phone', help='This field cannot be blank', required=True, type=str)


class SendSMSCode(Resource):
    def post(self):
        arguments = sending_parser.parse_args()
        user_id = arguments['id']
        user = User.get_by_id(user_id)

        phone = arguments['phone']
        phone = phone.replace(' ', '+')

        user.set_phone(phone)

        client.messages.create(
            to=phone,
            from_=twilio_phone,
            body=f'Twój kod weryfikacyjny w serwisie Zakupy Dla Seniora to: { user.verification_code }.'
        )

        user.set_code_sent()
        user.save()

        return {'success': True, 'code': user.verification_code, 'number': user.phone}, 200


checking_parser = reqparse.RequestParser()
checking_parser.add_argument('user_id', help='This field cannot be blank', required=True)
checking_parser.add_argument('verification_code', help='This field cannot be blank.', required=True, type=int)


class CheckSMSCode(Resource):
    def post(self):
        arguments = checking_parser.parse_args()
        user_id = arguments['user_id']
        verification_code = arguments['verification_code']

        user = User.get_by_id(user_id)

        if user.verification_code == verification_code:
            user.set_verified()
            user.save()
            return {'success': True, 'id': user.id, 'verified': user.verified}, 200
        else:
            return {'success': False, 'message': 'Zły kod weryfikacyjny.'}, 401
