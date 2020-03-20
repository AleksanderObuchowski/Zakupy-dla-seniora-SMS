from flask_restful import Resource, reqparse
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token
from zakupy_dla_seniora.sms_handler.models import Messages
from zakupy_dla_seniora.sms_handler.functions import get_location
from zakupy_dla_seniora.sms_handler.dialog_functions import *
client = Client(twilio_sid, twilio_auth_token)
twilio_phone = '+12057109660'

sending_parser = reqparse.RequestParser()
sending_parser.add_argument('Body', help='This field cannot be blank.', required=True, type=str)
sending_parser.add_argument('From', help='This field cannot be blank.', required=True, type=str)


class ReceiveSMS(Resource):
    def post(self):
        message_content = sending_parser.parse_args()['Body']
        phone_number = sending_parser.parse_args()['From']
        last_message  = Messages.get_by_phone(phone_number)

        if last_message:
            if last_message.message_status == 'Waiting for location':
                response_message = got_location_message(last_message,message_content)
            else:
                response_message = new_message(message_content, phone_number)

        else:
            response_message = new_message(message_content, phone_number)


        try:
            client.messages.create(
                to=phone_number,
                from_=twilio_phone,
                body=response_message
            )
            response_sent = True
        except:
            response_sent = False


        return {'success': True, 'response': response_message,'response_sent': response_sent}, 200
