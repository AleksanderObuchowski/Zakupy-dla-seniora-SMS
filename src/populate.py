import requests
from faker import Faker
from random import randint
import time
from datetime import datetime


local_url = 'http://127.0.0.1:5001'
fake = Faker(['pl_PL'])
added_users = []
added_messages = []


def create_users(amount):
    endpoint = '/register'
    for i in range(amount):
        name = fake.name()
        full_name = name.split(' ')
        first_name = full_name[0]
        last_name = full_name[1]
        password = 'example_pass'
        phone = f'+48{randint(100000000, 999999999)}'
        r = requests.post(
            f'{local_url}{endpoint}',
            data={
                'name': name,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
                'phone': phone
            }
        )
        print(f'Added User: {name}.')
        added_users.append(r.json()['id'])
        time.sleep(0.5)


def create_messages(amount):
    endpoint = '/sms'
    products = [
        'mleko', 'masło', 'chleb', 'mydło', 'ibuprom', 'lek na nadciśnienie',
        'jajka', 'papryka', 'cebula', 'ziemniaki', 'ketchup', 'musztarda',
        'majonez', 'jajko', 'margaryna', 'mięso', 'kurczak', 'kaszanka'
    ]

    locations = [
        'Gdańsk Zaspa', 'Gdańsk Wrzeszcz', 'Gdańsk Przymorze', 'Warszawa',
        'Gdańsk', 'Poznań', 'Wrocław', 'Łódź', 'Toruń', 'Bydgoszcz',
        'Szczecin', 'Gdynia', 'Olsztyn', 'Kraków', 'Rzeszów'
    ]

    for i in range(amount):
        # products_num = randint(1, len(products_num) - 1)
        products_num = randint(1, 3)
        body = 'Proszę kupić '
        for _ in range(products_num):
            body += products[randint(0, len(products) - 1)]
            body += ' '
        body += ', lokalizacja : ' + locations[randint(0, len(locations) - 1)]
        from_ = f'+48{randint(100000000, 999999999)}'

        r = requests.post(
            f'{local_url}{endpoint}',
            data={
                'Body': body,
                'From': from_
            }
        )
        print(f'Added Message "{body}".')
        added_messages.append(r.json()['id'])
        time.sleep(0.5)


def create_placings(amount):
    endpoint = '/placing'

    for i in range(amount):
        user_id = added_users[randint(0, len(added_users) - 1)]
        message_id = added_messages[randint(0, len(added_messages) - 1)]

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
    amount_ = 10
    create_users(amount_)
    create_messages(amount_)
    create_placings(amount_)

