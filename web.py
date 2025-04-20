import requests
import geocoder

def get_weather(lat, lon):
    api_key = 'c5208326b2a8c1c5a427f88f451d8705'
    api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    json_data = requests.get(api_url).json()
    temperature = round(json_data["main"]["temp"] - 273.15)  # Convert temperature to Celsius
    description = json_data["weather"][0]["description"]
    return temperature, description

def get_current_location():
    g = geocoder.ip('me')
    return g.latlng

def get_weather_by_location(location):
    g = geocoder.arcgis(location)
    lat, lon = g.latlng
    return get_weather(lat, lon)
