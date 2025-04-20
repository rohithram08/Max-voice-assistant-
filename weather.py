import os
import requests
import geocoder
from requests.exceptions import HTTPError, ConnectionError

# Load the API key from an environment variable
API_KEY = os.getenv('fa6392c7e14e1b0dd334745018859bb2')

def get_weather(lat, lon):
    api_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        json_data = response.json()
        temperature = json_data["main"]["temp"]
        description = json_data["weather"][0]["description"]
        return temperature, description
    except (HTTPError, ConnectionError) as e:
        print(f"HTTP or connection error occurred: {e}")
        return None, None
    except KeyError as e:
        print(f"Key error occurred: {e}")
        return None, None

def get_current_location():
    try:
        g = geocoder.ip('me')
        return g.latlng
    except Exception as e:
        print(f"Error getting current location: {e}")
        return None

def get_weather_by_location(location):
    try:
        g = geocoder.arcgis(location)
        if g.latlng:
            lat, lon = g.latlng
            return get_weather(lat, lon)
        else:
            print(f"Could not find the location: {location}")
            return None, None
    except Exception as e:
        print(f"Error getting weather by location: {e}")
        return None, None

def get_weather_info(location=None):
    if location is None or location.lower() == "current place":
        latlng = get_current_location()
        if latlng:
            lat, lon = latlng
            return get_weather(lat, lon)
        else:
            print("Could not determine current location.")
            return None, None
    else:
        return get_weather_by_location(location)

# Example usage:
# Set your API key in the environment variable 'OPENWEATHER_API_KEY' before running the script.
# weather_info = get_weather_info("current place")  # For current location
# weather_info = get_weather_info("New York")       # For a specific location
# print(weather_info)
