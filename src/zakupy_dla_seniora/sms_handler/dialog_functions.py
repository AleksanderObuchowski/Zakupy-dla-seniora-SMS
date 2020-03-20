from zakupy_dla_seniora.sms_handler.models import Messages
from zakupy_dla_seniora.sms_handler.functions import get_location
from zakupy_dla_seniora.orders.models import Orders


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
