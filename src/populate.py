import requests
from faker import Faker
from random import randint
import time
from datetime import datetime
from text_unidecode import unidecode


local_url = 'http://127.0.0.1:5000'
fake = Faker(['pl_PL'])
added_users = []
added_messages = []


def create_users(amount):
    endpoint = '/register'
    for i in range(amount):
        name = fake.name()
        r = requests.post(
            f'{local_url}{endpoint}',
            data={
                'displayName': name,
                'email': '.'.join(name.split(' ')) + '@gmail.com',
                'id': unidecode(''.join(fake.uuid4()))
            }
        )
        print(f'Added User: {name}.')
        added_users.append(r.json()['id'])
        time.sleep(0.5)


def create_messages(amount):
    endpoint = '/sms'
    begin_phrases = [
        "Dzień dobry, poproszę", "Potrzebuję ", "", "O to moja lista zakupów"
    ]

    num_products = [
        "pół", "jeden", "dwa", "dwie", "trzy", "cztery", "pięć", "sześć", "siedem", "osiem", "dziewięć",
        "dwadzieścia jeden", "trzydzieści pięć"
    ]

    products = [
        'l mleka', 'kostki masła', 'bochenki chleba', 'mydła', 'ibupromy', 'lek na ból gardła',
        'jajka', 'papryka', 'cebula', ' kg ziemniaków', 'ketchupy', 'musztardy',
        'majonezy', ' jajka', 'margaryny', 'kg mięsa', 'kurczaki', 'bułki'
    ]

    location_phrases = [
        ", lokalizacja: ", "mieszkam w ", "proszę przywieźć do ", "mój adres to"
    ]

    cities = [
        'Gdańsk', 'Warszawa'
    ]

    districts_gdansk = [
        "Aniołki", "Brętowo", "Brzeźno", "Chełm", "Jasień", "Kokoszki", "Krakowiec - Górki Zachodnie",
        "Letnica", "Matarnia", "Młyniska", "Nowy Port", "Oliwa", "Olszynka",
        "Orunia Górna - Gdańsk Południe", "Orunia - Św.Wojciech - Lipce", "Osowa", "Piecki - Migowo",
        "Przeróbka", "Przymorze Małe", "Przymorze Wielkie", "Rudniki", "Siedlce", "Stogi", "Strzyża",
        "Suchanino", "Śródmieście", "Ujeścisko - Łostowice", "VII Dwór", "Wrzeszcz Dolny",
        "Wrzeszcz Górny", "Wyspa Sobieszewska", "Wzgórze Mickiewicza", "Zaspa - Młyniec",
        "Zaspa - Rozstaje", "Żabianka - Wejhera - Jelitkowo - Tysiąclecia"
    ]
    districts_warszawa = [
        "Mokotów", "Praga-Południe", "Ursynów", "Wola", "Bielany", "Targówek", "Bemowo", "Śródmieście", "Białołęka",
        "Ochota", "Wawer", "Praga-Północ", "Ursus", "Żoliborz", "Włochy", "Wilanów", "Wesoła", "Rembertów"
    ]

    for i in range(amount):
        # products_num = randint(1, len(products_num) - 1)
        products_num = randint(1, 3)
        body = begin_phrases[randint(0, len(begin_phrases)-1)] + " "
        verbally = randint(0, 1)
        numerals = num_products if verbally else range(1, 10)
        for _ in range(products_num):
            body += str(numerals[randint(0, len(numerals)-1)])
            body += " " + products[randint(0, len(products) - 1)] + ", "
        body += ' ' + location_phrases[randint(0, len(location_phrases)-1)]
        location = " " + cities[randint(0, len(cities) - 1)] + " "
        location += districts_gdansk[randint(0, len(districts_gdansk)-1)] if location == " Gdańsk " \
            else districts_warszawa[randint(0, len(districts_warszawa)-1)]
        body +=  location
        from_ = f'+48{randint(100000000, 999999999)}'

        r = requests.post(
            f'{local_url}{endpoint}',
            data={
                'Body': body,
                'From': from_
            }
        )
        print(f'Added Message "{body}".')
        time.sleep(0.5)


def create_placings(amount):
    endpoint = '/placing'

    for i in range(amount):
        user_id = added_users[randint(0, len(added_users) - 1)]
        message_id = randint(0, amount - 1)

        r = requests.post(
            f'{local_url}{endpoint}',
            data={
                'user_id': user_id,
                'message_id': message_id,
            }
        )
        print(f'Added Placing for {user_id} from {message_id}.')
        time.sleep(0.5)


if __name__ == '__main__':
    amount_ = 20
    # create_users(amount_)
    create_messages(amount_)
    # create_placings(amount_)
