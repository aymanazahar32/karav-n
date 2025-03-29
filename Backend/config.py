# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///camping.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    LIGHT_POLLUTION_API_KEY = os.getenv('LIGHT_POLLUTION_API_KEY')
    CAMPSITE_API_KEY = os.getenv('CAMPSITE_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # API Settings
    WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
    LIGHT_POLLUTION_API_URL = "https://api.lightpollutiondata.com/v1/data"
    CAMPSITE_API_URL = "https://api.campsite.com/v1/campsites"
    GEMINI_API_URL = "https://api.gemini.com/v1/complete"
    
    # Application Settings
    MAX_RECOMMENDATION_DISTANCE = 50  # km
    MAX_RECOMMENDATIONS = 10
    CACHE_TIMEOUT = 3600  # 1 hour in seconds
