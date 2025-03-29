# services/light_pollution_service.py

import requests
from flask import current_app

def get_light_pollution_level(lat, lon):
    """
    Retrieve light pollution level for the given coordinates.
    Implementation depends on your chosen API or data source.
    """
    api_key = current_app.config["LIGHT_POLLUTION_API_KEY"]
    if not api_key:
        return 5  # default or average level

    try:
        # Example, hypothetical:
        # url = f"https://api.lightpollutiondata.com/v1/data?lat={lat}&lon={lon}&apikey={api_key}"
        # response = requests.get(url)
        # data = response.json()
        # parse "darkness" or "brightness" index
        return 3  # mock value: 1=excellent, 9=poor
    except Exception as e:
        print(f"Light pollution API error: {e}")
        return 5
