from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)
API_KEY = os.getenv('API_KEY', default='36b96764a95f3dd9318b355da07e1ae7')

@app.route('/weather', methods=['GET'])
def get_weather():
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({'error': 'City parameter is missing.'}), 400

    weather_data = fetch_weather(city_name)
    if weather_data is None:
        return jsonify({'error': 'Failed to fetch weather data.'}), 500

    parsed_data = parse_weather(weather_data)
    if parsed_data is None:
        return jsonify({'error': 'Failed to parse weather data.'}), 500

    return jsonify(parsed_data)

def fetch_weather(city_name: str):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return weather_data
    except requests.RequestException:
        return None

def parse_weather(weather_data: dict):
    if weather_data is None:
        return None

    city_name = weather_data['name']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    desc = weather_data['weather'][0]['main']
    icon_code = weather_data['weather'][0]['icon']

    return {
        'city_name': city_name,
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed,
        'desc': desc,
        'icon_code': icon_code
    }

if __name__ == '__main__':
    app.run()
