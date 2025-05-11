# app.py
import requests
import csv
from datetime import datetime

API_KEY = '3cf6ed9a2c8762c3da4b7539d7c7ba79'
CITY = 'Lahore'
URL = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

def fetch_weather():
    response = requests.get(URL)
    data = response.json()

    return {
        'Date and Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Temperature': data['main']['temp'],
        'Humidity': data['main']['humidity'],
        'Wind Speed': data['wind']['speed'],
        'Weather Condition': data['weather'][0]['description']
    }
# test
def save_to_csv(entry, filename = 'data/raw_data.csv'):
    file_exists = False
    try:
        with open(filename, 'r'):
            file_exists = True
    except FileNotFoundError:
        pass

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)


if __name__ == "__main__":
    weather = fetch_weather()
    save_to_csv(weather)
