import googlemaps
from flask import current_app
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

def get_maps_client():
    """Initialize Google Maps client"""
    api_key = current_app.config["GOOGLE_MAPS_API_KEY"]
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY is not configured")
    return googlemaps.Client(key=api_key)

def get_location_details(address):
    """Get coordinates from address using Geopy"""
    try:
        geolocator = Nominatim(user_agent="camping_app")
        location = geolocator.geocode(address)
        if location:
            return {
                "lat": location.latitude,
                "lon": location.longitude,
                "address": location.address
            }
        return None
    except GeocoderTimedOut:
        return None

def get_nearby_places(lat, lon, radius=50000, place_type="campground"):
    """Get nearby places using Google Places API"""
    try:
        gmaps = get_maps_client()
        places_result = gmaps.places_nearby(
            location=(lat, lon),
            radius=radius,
            type=place_type
        )
        
        places = []
        while places_result.get('results'):
            for place in places_result['results']:
                # Get detailed place information
                place_details = gmaps.place(place['place_id'], fields=[
                    'name', 'rating', 'formatted_address', 'geometry',
                    'opening_hours', 'photos', 'website', 'formatted_phone_number'
                ])['result']
                
                # Get directions to the place
                directions = gmaps.directions(
                    origin=f"{lat},{lon}",
                    destination=place['place_id'],
                    mode="driving"
                )
                
                places.append({
                    "name": place_details.get('name'),
                    "address": place_details.get('formatted_address'),
                    "location": place_details.get('geometry', {}).get('location'),
                    "rating": place_details.get('rating'),
                    "is_open": place_details.get('opening_hours', {}).get('open_now'),
                    "photos": place_details.get('photos', []),
                    "website": place_details.get('website'),
                    "phone": place_details.get('formatted_phone_number'),
                    "directions": directions[0] if directions else None
                })
            
            # Check if there are more results
            if 'next_page_token' in places_result:
                time.sleep(2)  # Wait before requesting next page
                places_result = gmaps.places_nearby(
                    location=(lat, lon),
                    radius=radius,
                    type=place_type,
                    page_token=places_result['next_page_token']
                )
            else:
                break
                
        return places
    except Exception as e:
        current_app.logger.error(f"Google Maps API error: {str(e)}")
        return []

def get_hiking_trails(lat, lon, radius=50000):
    """Get nearby hiking trails"""
    try:
        gmaps = get_maps_client()
        trails_result = gmaps.places_nearby(
            location=(lat, lon),
            radius=radius,
            type="park",
            keyword="hiking trail"
        )
        
        trails = []
        while trails_result.get('results'):
            for trail in trails_result['results']:
                # Get detailed trail information
                trail_details = gmaps.place(trail['place_id'], fields=[
                    'name', 'rating', 'formatted_address', 'geometry',
                    'opening_hours', 'photos', 'website', 'formatted_phone_number',
                    'reviews'
                ])['result']
                
                # Get directions to the trail
                directions = gmaps.directions(
                    origin=f"{lat},{lon}",
                    destination=trail['place_id'],
                    mode="driving"
                )
                
                trails.append({
                    "name": trail_details.get('name'),
                    "address": trail_details.get('formatted_address'),
                    "location": trail_details.get('geometry', {}).get('location'),
                    "rating": trail_details.get('rating'),
                    "reviews": trail_details.get('reviews', []),
                    "is_open": trail_details.get('opening_hours', {}).get('open_now'),
                    "photos": trail_details.get('photos', []),
                    "website": trail_details.get('website'),
                    "phone": trail_details.get('formatted_phone_number'),
                    "directions": directions[0] if directions else None
                })
            
            # Check if there are more results
            if 'next_page_token' in trails_result:
                time.sleep(2)  # Wait before requesting next page
                trails_result = gmaps.places_nearby(
                    location=(lat, lon),
                    radius=radius,
                    type="park",
                    keyword="hiking trail",
                    page_token=trails_result['next_page_token']
                )
            else:
                break
                
        return trails
    except Exception as e:
        current_app.logger.error(f"Google Maps API error: {str(e)}")
        return [] 