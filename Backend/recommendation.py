# recommendation.py

import math
from services.weather_service import get_weather
from services.light_pollution_service import get_light_pollution_level
from services.maps_service import get_nearby_places, get_hiking_trails
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
    1) Fetch nearby campsites and hiking trails using Google Maps
    2) Get weather and light pollution data for each location
    3) Filter and score based on user preferences
    4) Generate AI recommendations
    """
    # 1) Get potential locations
    campsites = get_nearby_places(user_lat, user_lon, radius=50000, place_type="campground")
    hiking_trails = get_hiking_trails(user_lat, user_lon, radius=50000)
    
    # 2) Process each location
    results = []
    for site in campsites:
        # Get weather and light pollution data
        weather = get_weather(site["location"]["lat"], site["location"]["lng"])
        lp_data = get_light_pollution_level(site["location"]["lat"], site["location"]["lng"])
        
        # Calculate distance
        distance = haversine_distance(
            user_lat, user_lon,
            site["location"]["lat"], site["location"]["lng"]
        )
        
        # Calculate base score
        base_score = 10
        
        # Weather factors
        if weather["temp"] and 15 <= weather["temp"] <= 25:  # Ideal temperature range
            base_score += 2
        if weather["clouds"] and weather["clouds"] < 30:  # Clear skies
            base_score += 2
        if not weather["rain"]:
            base_score += 1
            
        # Light pollution factors
        if lp_data["level"] >= 8:  # Excellent for stargazing
            base_score += 3
        elif lp_data["level"] >= 6:  # Good for stargazing
            base_score += 2
            
        # Distance factor (penalize longer distances)
        base_score -= (distance / 10)
        
        # User preference factors
        if user_preferences.get("prefers_fishing") and "fishing" in site.get("amenities", []):
            base_score += 2
        if user_preferences.get("prefers_hiking"):
            # Check for nearby hiking trails
            nearby_trails = [t for t in hiking_trails 
                           if haversine_distance(
                               site["location"]["lat"], site["location"]["lng"],
                               t["location"]["lat"], t["location"]["lng"]
                           ) < 5]  # Within 5km
            if nearby_trails:
                base_score += 2
        if user_preferences.get("prefers_solitude") and not site.get("is_open", True):
            base_score += 1
            
        # Add location to results
        results.append({
            "name": site["name"],
            "address": site["address"],
            "location": site["location"],
            "distance": distance,
            "weather": weather,
            "light_pollution": lp_data,
            "rating": site.get("rating", 0),
            "is_open": site.get("is_open", True),
            "photos": site.get("photos", []),
            "website": site.get("website"),
            "phone": site.get("phone"),
            "directions": site.get("directions"),
            "score": base_score
        })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Get top locations for AI recommendation
    top_spots = results[:5]
    top_spots_text = "\n".join([
        f"{idx+1}. {spot['name']} (score: {spot['score']:.2f})\n"
        f"   Weather: {spot['weather']['description']}, "
        f"Temperature: {spot['weather']['temp']}°C\n"
        f"   Light Pollution: {spot['light_pollution']['level']}/10\n"
        f"   Distance: {spot['distance']:.1f}km"
        for idx, spot in enumerate(top_spots)
    ])
    
    # Generate AI recommendation
    prompt = f"""User preferences: {user_preferences}
Top camping spots:\n{top_spots_text}\n
Based on the weather conditions, light pollution levels, and user preferences,
which campsite would be the best choice and why? Consider:
1. Weather conditions for camping and stargazing
2. Light pollution levels for stargazing
3. Distance and accessibility
4. User preferences (fishing, hiking, solitude)
Provide a detailed recommendation with specific reasons.
"""
    ai_summary = get_ai_recommendation(prompt)
    
    return {
        "results": results,
        "ai_summary": ai_summary,
        "hiking_trails": hiking_trails
    }
