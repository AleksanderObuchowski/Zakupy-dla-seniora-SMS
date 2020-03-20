import requests

import spacy
from spacy import displacy

nlp = spacy.load('pl_model')

geocoder_url = 'https://us1.locationiq.com/v1/search.php'
geocoder_api = '81a3bf223e5959'
geocoder_data = {
    'key': geocoder_api,
    'q': '',
    'format': 'json'
}


def get_location(message,search = True):
    if search:
        doc = nlp(message)
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                location_text = ent.text
                geocoder_data['q'] = location_text
                location = requests.get(geocoder_url, params=geocoder_data)
                if not 'error' in location.json():
                    lat = float(location.json()[0]['lat'])
                    lon = float(location.json()[0]['lon'])
                    return location_text, lat, lon
        return 'unk','unk','unk'
    else:
        geocoder_data['q'] = message
        location = requests.get(geocoder_url, params=geocoder_data)
        if not 'error' in location.json():
            print(location.json())
            lat = float(location.json()[0]['lat'])
            lon = float(location.json()[0]['lon'])
            return message, lat, lon
        else:
            return 'unk', 'unk', 'unk'


if __name__ == '__main__':
    get_location("Poprosze kupić masło Kasia 2 opakowania pozdranwiam Halina Mostowiak, lokalizacja : Gdańsk Zaspa")
