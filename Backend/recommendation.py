# recommendation.py

import math
from services.weather_service import get_weather
from services.light_pollution_service import get_light_pollution_level
from services.campsite_service import get_nearby_campsites
from services.gemini_service import get_ai_recommendation

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def recommend_campsites(user_lat, user_lon, user_preferences):
    """
    1) Fetch nearby campsites within a certain radius.
    2) Retrieve weather and light pollution for each site.
    3) Filter based on user preferences, availability, etc.
    4) Sort or rank them by some heuristic.
    5) (Optional) Summarize with Gemini or another LLM.
    """
    # 1) Get potential campsites
    candidate_campsites = get_nearby_campsites(user_lat, user_lon)

    # 2) For each campsite, gather additional data
    results = []
    for site in candidate_campsites:
        weather = get_weather(site["lat"], site["lon"])
        lp_level = get_light_pollution_level(site["lat"], site["lon"])
        distance = haversine_distance(user_lat, user_lon, site["lat"], site["lon"])

        # 3) Filter out if not available (and user requires availability)
        if not site["availability"] and user_preferences.get("require_availability", False):
            continue

        # 4) Simple scoring
        # Lower light pollution => better
        # Also factor in distance, user preferences (fishing, hiking, solitude, etc.)
        # Example: Subtract one point for every 10km
        # Subtract lp_level from 10 => higher is better
        # Check if "fishing" is in site amenities if user prefers fishing, etc.
        base_score = 10 - lp_level  # if lp_level=1 => score=9; if lp_level=5 => score=5 ...
        base_score -= (distance / 10)

        # If user prefers solitude, remove sites with large facilities (mock).
        # If user prefers fishing, check if "fishing" is an amenity.
        # etc. This is just an example:
        if user_preferences.get("prefers_fishing") and "fishing" in site.get("amenities", []):
            base_score += 2
        if user_preferences.get("prefers_hiking") and "hiking_trails" in site.get("amenities", []):
            base_score += 2
        # ... you can add more logic.

        results.append({
            "name": site["name"],
            "distance": distance,
            "light_pollution_level": lp_level,
            "weather": weather,
            "availability": site["availability"],
            "score": base_score
        })

    # Sort by score desc
    results.sort(key=lambda x: x["score"], reverse=True)

    # 5) Optionally ask Gemini for a final textual recommendation
    top_spots_text = "\n".join([f"{idx+1}. {res['name']} (score: {res['score']:.2f})" for idx, res in enumerate(results[:5])])
    prompt = f"""User preferences: {user_preferences}.
Candidate campsites:\n{top_spots_text}\n
Which campsite is best for the user and why? Provide a succinct recommendation.
"""
    ai_summary = get_ai_recommendation(prompt)

    return {
        "results": results,
        "ai_summary": ai_summary
    }
