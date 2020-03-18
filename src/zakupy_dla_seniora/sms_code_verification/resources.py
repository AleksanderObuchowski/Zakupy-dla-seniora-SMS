from flask_restful import Resource, reqparse
from twilio.rest import Client
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token

client = Client(twilio_sid, twilio_auth_token)

sending_parser = reqparse.RequestParser()
sending_parser.add_argument('phone_number', help='This field cannot be blank.', required=True, type=str)


class SendSMSCode(Resource):
    def post(self):
        phone = sending_parser.parse_args()['phone_number']
        phone = phone.replace(' ', '+')
        user = User.get_by_phone(phone)

        client.messages.create(
            to=phone,
            from_='+18317049826',
            body=f'Twój kod weryfikacyjny w serwisie Zakupy Dla Seniora to: { user.verification_code }.'
        )

        return {'success': True, 'code': user.verification_code, 'number': user.phone}, 200


checking_parser = reqparse.RequestParser()
checking_parser.add_argument('phone_number', help='This field cannot be blank.', required=True, type=str)
checking_parser.add_argument('verification_code', help='This field cannot be blank.', required=True, type=int)


class CheckSMSCode(Resource):
    def post(self):
        arguments = checking_parser.parse_args()
        phone = arguments['phone_number']
        phone = phone.replace(' ', '+')
        verification_code = arguments['verification_code']

        user = User.get_by_phone(phone)

        if user.verification_code == verification_code:
            user.verified = True
            user.save()
            return {'success': True}, 200
        else:
            return {'success': False, 'message': 'Zły kod weryfikacyjny.'}, 401





