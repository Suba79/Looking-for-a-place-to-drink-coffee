import json
import requests
coordinates = input("Где вы находитесь? ")

def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


# with open("coffee.json", "r", encoding="cp1251") as my_file:
#     data = json.load(my_file)  # Чтение и парсинг в одном шаге
    
# # Предполагаем, что data - это список словарей
# for item in data:
#     print(item['Name'])
#     print(item['geoData']['coordinates'][0])
#     print(item['geoData']['coordinates'][1])
#     print("-" * 20)  # Разделитель между записями
