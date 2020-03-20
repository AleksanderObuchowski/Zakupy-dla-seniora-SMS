from zakupy_dla_seniora.sms_handler.models import Messages
from zakupy_dla_seniora.sms_handler.functions import get_location
from zakupy_dla_seniora.placings.models import Placings
from zakupy_dla_seniora.users.models import  User
from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token
from twilio.rest import Client
twilio_phone = '+12057109660'


client = Client(twilio_sid, twilio_auth_token)

def new_message( message_content, phone_number):
    message_location, lat, lon = get_location(message_content)
    if message_location == 'unk':
        new_message = Messages(
            message_content=message_content,
            phone_number=phone_number,
            message_status='Waiting for location'
        )
        new_message.save()
        response_message = 'Nie wyłapaliśmy lokalizacji w twoim zamówieniu, czy możesz podać ją jeszcze raz w formacie [Miasto, Dzielnica]?'
        return response_message

    else:
        new_message = Messages(
            message_content=message_content,
            phone_number=phone_number,
            message_location=message_location,
            message_location_lat=lat,
            message_location_lon=lon,
        )
        new_message.save()
        response_message = 'Twoje zamówienie zostało przyjęte, czekamy aż ktoś się zgłosi'

        return response_message

def got_location_message(last_message, message_content):
    message_location, lat, lon = get_location(message_content, search = False)
    if message_location != 'unk':
        last_message.message_location = message_location
        last_message.message_location_lat = lat
        last_message.message_location_lon = lon
        last_message.message_status = 'Recieved'
        last_message.save()
        response_message = 'Twoje zamówienie zostało przyjęte, czekamy aż ktoś się zgłosi'
    else:
        response_message = 'Nadal nie wyłapaliśmy twojej lokalizacji spróbuj jeszcze raz'


    return response_message

def placing_creation_message(user_id,message_id):
    message = Messages.get_by_id(message_id)
    user = User.get_by_id(user_id)
    response_message = f'Użytkownik {user.name} {user.last_name} o numerze telefonu {user.phone} zgłosił sie aby' \
                       f' zrealizować twoje zamówienie, prosze podaj dokładny adres'
    message.message_status = 'Waiting for address';
    message.save()

    try:
        client.messages.create(
            to=message.phone_number,
            from_=twilio_phone,
            body=response_message
        )
        response_sent = True
    except:
        response_sent = False
    return {'success': True, 'response': response_message,'response_sent': response_sent}, 200

def got_address_message(last_message, message_content):
    last_message.message_precise_location = message_content
    last_message.message_status = "Adress given"
    last_message.save()

    response_message= f'Wolontariusz został poinformowany o twoim adresie, niedługo możesz spodziewać sie zakupów!'
    try:
        client.messages.create(
            to=last_message.phone_number,
            from_=twilio_phone,
            body=response_message
        )
        response_sent = True
    except:
        response_sent = False
    return {'success': True, 'response': response_message,'response_sent': response_sent}, 200
