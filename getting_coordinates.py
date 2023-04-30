import requests
import random


def getting(response):
    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        return [str(toponym_longitude), str(toponym_lattitude)]
    except BaseException:
        return False


def generate_city(name_city):
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name_city,
        "format": "json"}

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    response = requests.get(geocoder_api_server, params=geocoder_params)

    tompony = getting(response)

    address_ll = ','.join(tompony)

    delta = "0.009"

    l = 'map'

    map_params = {
        "ll": address_ll,
        "spn": ",".join([delta, delta]),
        "l": l,
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    return response
