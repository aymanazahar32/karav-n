# services/campsite_service.py

import requests
from flask import current_app

def get_nearby_campsites(lat, lon, max_distance=50):
    """
    Query an external campsite reservation system or DB.
    Return a list of campsite info dicts, including availability.
    """
    api_key = current_app.config["CAMPSITE_API_KEY"]
    if not api_key:
        # Return some mocked data
        return [
            {
                "name": "Mock Campground A",
                "lat": lat + 0.1,
                "lon": lon + 0.1,
                "distance": 10,
                "amenities": ["water", "restrooms", "fire_pit"],
                "availability": True
            },
            {
                "name": "Mock Campground B",
                "lat": lat + 0.2,
                "lon": lon + 0.2,
                "distance": 20,
                "amenities": ["electricity", "showers"],
                "availability": False
            }
        ]

    # Real logic with your chosen API:
    # ...
    return []
