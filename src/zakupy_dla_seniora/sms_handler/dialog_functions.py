from zakupy_dla_seniora.sms_handler.models import Messages
from zakupy_dla_seniora.sms_handler.functions import get_location
from zakupy_dla_seniora.placings.models import Placings
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora.config import twilio_sid, twilio_auth_token
from twilio.rest import Client
from zakupy_dla_seniora.config import twilio_phone

client = Client(twilio_sid, twilio_auth_token)


def new_message(message_content, phone_number):
    message_location, lat, lon = get_location(message_content)
    if message_location == 'unk':
        db_new_message = Messages(
            message_content=message_content,
            phone_number=phone_number,
            message_status='Waiting for location'
        )
        db_new_message.save()
        response_message = 'Nie wyłapaliśmy lokalizacji w twoim zamówieniu, czy możesz podać ' \
                           'ją jeszcze raz w formacie [Miasto, Dzielnica]?'
        return response_message

    else:
        db_new_message = Messages(
            message_content=message_content,
            phone_number=phone_number,
            message_location=message_location,
            message_location_lat=lat,
            message_location_lon=lon,
        )
        db_new_message.save()
        response_message = 'Twoje zamówienie zostało przyjęte, czekamy aż ktoś się zgłosi.'

        return response_message


def got_location_message(last_message, message_content):
    message_location, lat, lon = get_location(message_content, search=False)
    if message_location != 'unk':
        last_message.message_location = message_location
        last_message.message_location_lat = lat
        last_message.message_location_lon = lon
        last_message.message_status = 'Received'
        last_message.save()
        response_message = 'Twoje zamówienie zostało przyjęte, czekamy aż ktoś się zgłosi.'
    else:
        response_message = 'Nadal nie wyłapaliśmy twojej lokalizacji, spróbuj jeszcze raz.'

    return response_message


def placing_creation_message(user_id, message_id):
    message = Messages.get_by_id(message_id)
    user = User.get_by_id(user_id)
    response_message = f'Użytkownik {user.display_name} o numerze telefonu {user.phone} zgłosił się, aby' \
                       f' zrealizować twoje zamówienie, prosze podaj dokładny adres.'
    message.message_status = 'Waiting for address'
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
    return {'success': True, 'response': response_message, 'response_sent': response_sent}, 200


def got_address_message(last_message, message_content):
    last_message.message_precise_location = message_content
    last_message.message_status = "Adress given"
    last_message.save()

    response_message = f'Wolontariusz został poinformowany o twoim adresie, niedługo możesz spodziewać sie zakupów!'
    placing = Placings.query.filter(Placings.message_id == last_message.id).order_by(
        Placings.placing_date.desc()).first()
    placing.placing_status = "Adress given"
    print(placing.id)
    placing.save()
    try:
        client.messages.create(
            to=last_message.phone_number,
            from_=twilio_phone,
            body=response_message
        )
        response_sent = True
    except:
        response_sent = False
    return {'success': True, 'response': response_message, 'response_sent': response_sent}, 200


def ending_approval_message(user_id, message_id):
    last_message = Messages.get_by_id(message_id)
    last_message.message_status = "waiting for ending approval"
    last_message.save()

    response_message = f'Czy twoje zakupy zostały dostarczone pomyślnie? Odpisz TAK jeżeli' \
                       f' wszystko poszło dobrze, lub opisz nam swoje problemy.'
    try:
        client.messages.create(
            to=last_message.phone_number,
            from_=twilio_phone,
            body=response_message
        )
        response_sent = True
    except:
        response_sent = False
    return {'success': True, 'response': response_message, 'response_sent': response_sent}, 200


def got_final_confirmation(last_message, message_content):
    if message_content.lower() in ['tak', 'dobrze', 'spoko', 'super']:
        last_message.message_status = "Done"
        last_message.save()
        placing = Placings.query.filter(Placings.message_id == last_message.id).order_by(
            Placings.placing_date.desc()).first()
        user_id = placing.user_id
        placing.status = "Done"
        placing.save()
        user = User.query.filter(User.id == user_id).first()
        user.points += 10
        user.save()
        response_message = "Dziękujemy za skorzystanie z naszego systemu czekamy na kolejne zamówienie."
        return response_message
    else:
        last_message.message_status = "Something worng"
        last_message.save()
        placing = Placings.query.filter(Placings.message_id == last_message.id).order_by(
            Placings.placing_date.desc()).first()
        placing.status = "Something worng"
        placing.save()
        response_message = "Dziękujemy za informacje, moderacja przyjrzy się sprawie."
        return response_message
