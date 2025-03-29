# services/weather_service.py

import os
import requests
from flask import current_app
from functools import lru_cache
import time

@lru_cache(maxsize=100)
def get_weather(lat, lon):
    """
    Fetch weather data from OpenWeatherMap API.
    Cached for 1 hour to avoid excessive API calls.
    """
    api_key = current_app.config["WEATHER_API_KEY"]
    if not api_key:
        raise ValueError("WEATHER_API_KEY is not configured")

    # Validate coordinates
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("Invalid latitude or longitude")

    try:
        url = current_app.config["WEATHER_API_URL"]
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract relevant weather data
        weather = {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "clouds": data["clouds"]["all"],
            "rain": "rain" in data if "rain" in data else False,
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "timestamp": int(time.time())
        }
        
        return weather
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Weather API error: {str(e)}")
        return {
            "temp": None,
            "description": "unavailable",
            "clouds": None,
            "rain": None,
            "humidity": None,
            "wind_speed": None,
            "timestamp": int(time.time())
        }
    except (KeyError, ValueError) as e:
        current_app.logger.error(f"Weather data parsing error: {str(e)}")
        return {
            "temp": None,
            "description": "data error",
            "clouds": None,
            "rain": None,
            "humidity": None,
            "wind_speed": None,
            "timestamp": int(time.time())
        }
