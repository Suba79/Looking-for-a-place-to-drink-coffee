import json
import requests
from geopy import distance
from dotenv import load_dotenv
import os
from pprint import pprint
import folium


load_dotenv()
apikey = os.getenv("YANDEX_GEOCODE_API_KEY")


def fetch_coordinates(apikey, address):
    """Получаем координаты адреса через Yandex API."""
    base_url = "https://geocode-maps.yandex.ru/1.x"
    try:
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
        return float(lat), float(lon)
    except Exception as e:
        print(f"Ошибка при геокодировании адреса {address}: {e}")
        return None


def calculate_distance(coord1, coord2):
    """Вычисляем расстояние между двумя точками."""
    return distance.distance(coord1, coord2).km


def generate_coffee_map(user_coords, shops):
    """Генерирует HTML-файл с картой кофеен."""
    coffee_map = folium.Map(location=user_coords, zoom_start=14)

    folium.Marker(
        location=user_coords,
        popup="Вы здесь",
        icon=folium.Icon(color="red", icon="user")
    ).add_to(coffee_map)

    for shop in shops:
        folium.Marker(
            location=shop['coordinates'],
            popup=f"{shop['name']}<br>Расстояние: {shop['distance']:.2f} км",
            icon=folium.Icon(color="green", icon="coffee")
        ).add_to(coffee_map)

    coffee_map.save("coffee_map.html")


def main():
    try:
        with open("coffee.json", "r", encoding="cp1251") as file:
            coffee_shops = json.load(file)
    except FileNotFoundError:
        print("Файл coffee.json не найден!")
        return
    except json.JSONDecodeError:
        print("Ошибка в формате JSON!")
        return

    if not coffee_shops:
        print("Нет данных о кофейнях.")
        return

    user_address = input("Введите ваш адрес: ")
    user_coords = fetch_coordinates(apikey, user_address)
    if not user_coords:
        print("Не удалось определить координаты.")
        return

    print(f"\nВаши координаты: {user_coords}\n")

    shops_with_distances = []
    for shop in coffee_shops:
        try:
            name = shop.get("Name", "Без названия")
            address = shop.get("Address", "Адрес не указан")
            lat = float(shop["Latitude_WGS84"].replace(",", "."))
            lon = float(shop["Longitude_WGS84"].replace(",", "."))
            dist = calculate_distance(user_coords, (lat, lon))
            
            shops_with_distances.append({
                'name': name,
                'address': address,
                'distance': dist,
                'coordinates': (lat, lon)
            })
        except (ValueError, KeyError) as e:
            print(f"Ошибка в данных кофейни: {e}")
            continue

    if not shops_with_distances:
        print("Нет подходящих кофеен.")
        return

    nearest_shops = sorted(shops_with_distances, key=lambda x: x['distance'])[:5]

    print("\nБлижайшие кофейни:")
    for i, shop in enumerate(nearest_shops, 1):
        print(f"\n#{i}: {shop['name']}")
        pprint({
            'Адрес': shop['address'],
            'Расстояние (км)': round(shop['distance'], 2),
            'Координаты': shop['coordinates']
        })

    generate_coffee_map(user_coords, nearest_shops)

if __name__ == "__main__":
    main()
