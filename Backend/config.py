# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    LIGHT_POLLUTION_API_KEY = os.getenv("LIGHT_POLLUTION_API_KEY")
    CAMPSITE_API_KEY = os.getenv("CAMPSITE_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
