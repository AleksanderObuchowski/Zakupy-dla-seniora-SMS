from flask_restful import Resource, reqparse
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token
from zakupy_dla_seniora.sms_handler.models import Messages
from zakupy_dla_seniora.sms_handler.functions import get_location

client = Client(twilio_sid, twilio_auth_token)

sending_parser = reqparse.RequestParser()
sending_parser.add_argument('Body', help='This field cannot be blank.', required=True, type=str)
sending_parser.add_argument('From', help='This field cannot be blank.', required=True, type=str)


class ReceiveSMS(Resource):
    def post(self):
        message_content = sending_parser.parse_args()['Body']
        phone_number = sending_parser.parse_args()['From']

        message_location, lat, lon = get_location(message_content)
        new_message = Messages(
            message_content=message_content,
            phone_number=phone_number,
            message_location=message_location,
            message_location_lat=lat,
            message_location_lon=lon,
        )
        new_message.save()

        # client.messages.create(
        #     to=phone_number,
        #     from_='+12057109660',
        #     body= 'Twoje zamówienie zostało przyjęte, czekamy aż ktoś się zgłosi'
        # )

        return {'success': True}, 200
