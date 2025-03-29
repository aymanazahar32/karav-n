# services/weather_service.py

import os
import requests
from flask import current_app

def get_weather(lat, lon):
    """
    Fetch weather data from an external API.
    Replace with your actual logic and endpoint.
    """
    api_key = current_app.config["WEATHER_API_KEY"]
    if not api_key:
        return {
            "temp": None,
            "description": "API_KEY missing",
            "clouds": None,
            "rain": None
        }

    try:
        # Example using OpenWeatherMap:
        # url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        # response = requests.get(url)
        # data = response.json()
        # ...
        # Parse the data here:
        return {
            "temp": 15,
            "description": "clear sky",
            "clouds": 10,
            "rain": False
        }
    except Exception as e:
        print(f"Weather API error: {e}")
        return {
            "temp": None,
            "description": "unavailable",
            "clouds": None,
            "rain": None
        }
