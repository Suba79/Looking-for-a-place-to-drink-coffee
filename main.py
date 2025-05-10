import json

with open("coffee.json", "r", encoding="cp1251") as my_file:
    data = json.load(my_file)  # Чтение и парсинг в одном шаге
print(data[]['Name'])
print(data[]['geoData']['coordinates'][0])
print(data[]['geoData']['coordinates'][1])