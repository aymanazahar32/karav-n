# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from database import db
from models import User, CampReview
from recommendation import recommend_campsites
from services.maps_service import get_location_details, get_nearby_places, get_hiking_trails
from werkzeug.security import generate_password_hash, check_password_hash

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app)
    return app

app = create_app()

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    return jsonify({"message": "Welcome to Karaván! Where will the roads take you next?"})

# User sign-up
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = generate_password_hash(password)
    user = User(email=email, password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user": user.to_dict()})

# User login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "user": user.to_dict()})

# Update user preferences
@app.route("/api/preferences", methods=["POST"])
def update_preferences():
    data = request.json
    user_id = data.get("user_id")
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Just a small example. Extend as needed:
    user.prefers_fishing = data.get("prefers_fishing", False)
    user.prefers_hiking = data.get("prefers_hiking", False)
    user.prefers_solitude = data.get("prefers_solitude", False)

    db.session.commit()
    return jsonify({"message": "Preferences updated", "user": user.to_dict()})

# Get location details from address
@app.route("/api/location", methods=["GET"])
def get_location():
    address = request.args.get("address")
    if not address:
        return jsonify({"error": "Address is required"}), 400

    location = get_location_details(address)
    if not location:
        return jsonify({"error": "Location not found"}), 404

    return jsonify(location)

# Get nearby places
@app.route("/api/places", methods=["GET"])
def get_places():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    radius = request.args.get("radius", type=int, default=50000)
    place_type = request.args.get("type", default="campground")

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    places = get_nearby_places(lat, lon, radius, place_type)
    return jsonify(places)

# Get hiking trails
@app.route("/api/trails", methods=["GET"])
def get_trails():
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    radius = request.args.get("radius", type=int, default=50000)

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required"}), 400

    trails = get_hiking_trails(lat, lon, radius)
    return jsonify(trails)

# Get recommendations
@app.route("/api/recommendations", methods=["POST"])
def get_recommendations():
    data = request.json
    user_lat = data.get("lat")
    user_lon = data.get("lon")
    user_id = data.get("user_id")

    if not (user_lat and user_lon):
        return jsonify({"error": "Latitude and longitude are required"}), 400

    user = User.query.get(user_id) if user_id else None
    user_prefs = {}
    if user:
        # Build user preferences from DB
        user_prefs["prefers_fishing"] = user.prefers_fishing
        user_prefs["prefers_hiking"] = user.prefers_hiking
        user_prefs["prefers_solitude"] = user.prefers_solitude
    
    # Merge in any additional preferences from the request
    user_prefs.update(data.get("preferences", {}))

    recommendations = recommend_campsites(user_lat, user_lon, user_prefs)
    return jsonify(recommendations)

# Post a review
@app.route("/api/review", methods=["POST"])
def post_review():
    data = request.json
    user_id = data.get("user_id")
    campsite_name = data.get("campsite_name")
    rating = data.get("rating", 5)
    review_text = data.get("review_text", "")

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    review = CampReview(
        user_id=user_id,
        campsite_name=campsite_name,
        rating=rating,
        review_text=review_text
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({"message": "Review posted", "review": review.to_dict()})

# Get reviews for a campsite
@app.route("/api/reviews/<campsite_name>", methods=["GET"])
def get_reviews(campsite_name):
    reviews = CampReview.query.filter_by(campsite_name=campsite_name).all()
    return jsonify([r.to_dict() for r in reviews])

if __name__ == "__main__":
    app.run(debug=True)
