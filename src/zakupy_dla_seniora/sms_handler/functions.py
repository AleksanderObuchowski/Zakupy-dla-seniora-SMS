import requests
import spacy
import pandas as pd
import json
from zakupy_dla_seniora.sms_handler.word2numPL import words2num

nlp = spacy.load('pl_model')

geocoder_url = 'https://us1.locationiq.com/v1/search.php'
geocoder_api = '81a3bf223e5959'
geocoder_data = {
    'key': geocoder_api,
    'q': '',
    'format': 'json'
}


def get_location(message, search=True):
    if search:
        df = pd.read_csv("zakupy_dla_seniora/sms_handler/places.csv")
        doc = nlp(message.strip().title())
        products = []
        places_to_check = []
        location_text = ""
        used = []
        punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
        units = ["kg", "l", "litry", "dg", "dag", "g", "deko", "ml", "m", "cm"]
        for token in doc:
            if token.pos_ == "NUM":
                item = [token.text, token.head.text]
                used.append(token.text)
                used.append(token.head.text)
                if token.head.children:
                    for child in token.head.children:
                        if child.text not in used and child.dep_ != "conj":
                            item[1] += " " + child.text
                            used.append(child.text)
                    products.append(item)
            elif token.pos_ == "NOUN" and token.text not in used:
                places_to_check.append(token)
        places_to_check.reverse()

        for token in places_to_check:
            if location_text == "":
                if token.text in df.values:
                    location_text = token.text
                    used.append(token.text)
                    if token.children:
                        for child in token.children:
                            if child.text not in used and child.dep_ != "conj":
                                location_text += " " + child.text
                                if child in places_to_check:
                                    places_to_check.remove(child)
                                used.append(child.text)
                    if token.head.pos_ == "NOUN":
                        if token.head.text not in used:
                            location_text += " " + token.head.text
                            if token.head in places_to_check:
                                places_to_check.remove(token.head)
                            used.append(token.head.text)
                else:
                    if token.text not in used:
                        item = [1, token.text]
                        used.append(token.text)
                        if token.children:
                            for child in token.children:
                                if child.text not in used and child.dep_ != "conj":
                                    item[1] += " " + child.text
                                    used.append(child.text)
                                    products.append(item)
            if token.text not in used:
                item = [1, token.text]
                for child in token.children:
                    if child.text not in used and child.dep_ != "conj":
                        item[1] += " " + child.text
                        used.append(child.text)
                products.append(item)
        try:
            with open('zakupy_dla_seniora/sms_handler/products_ranking.json', "r") as jsonFile:
                products_json = json.load(jsonFile)
        except:
            products_json = {}
        for product in products:
            for letter in product[1]:
                if letter in punctuations:
                    product[1] = product[1].replace(letter, "")
            for word in product[1].split():
                if word in units:
                    product[1] = product[1].replace(word, "")
            try:
                product[0] = int(product[0])
            except:
                product[0] = words2num(product[0])
            if product[1] in products_json.keys():
                products_json[product[1]] += product[0]
            else:
                products_json[product[1]] = product[0]
        with open('zakupy_dla_seniora/sms_handler/products_ranking.json', "w+") as jsonFile:
            json.dump(products_json, jsonFile)

        if location_text != "":
            for letter in location_text:
                if letter in punctuations:
                    location_text = location_text.replace(letter, "")
            geocoder_data['q'] = location_text
            location = requests.get(geocoder_url, params=geocoder_data)
            if 'error' not in location.json():
                lat = float(location.json()[0]['lat'])
                lon = float(location.json()[0]['lon'])
                return location_text, lat, lon
        else:
            return 'unk', 'unk', 'unk'
    else:
        geocoder_data['q'] = message
        location = requests.get(geocoder_url, params=geocoder_data)
        if 'error' not in location.json():
            lat = float(location.json()[0]['lat'])
            lon = float(location.json()[0]['lon'])
            return message, lat, lon
        else:
            return 'unk', 'unk', 'unk'


if __name__ == '__main__':
    get_location("Proszę zawieźć 6 bułek pszennych, 3 zupy profi, domestos, do Gdańsk Zaspa")
