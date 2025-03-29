// src/api.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:5000/api" // Adjust if your Flask runs on a different port
});

// Auth
export const signup = (email, password) =>
  API.post("/signup", { email, password });
export const login = (email, password) =>
  API.post("/login", { email, password });

// Preferences
export const updatePreferences = (userId, prefs) =>
  API.post("/preferences", { user_id: userId, ...prefs });

// Reviews
export const postReview = (userId, campsiteName, rating, reviewText) =>
  API.post("/review", { user_id: userId, campsite_name: campsiteName, rating, review_text: reviewText });

export const getReviews = (campsiteName) =>
  API.get(`/reviews/${encodeURIComponent(campsiteName)}`);

// Recommendations
export const getRecommendations = (lat, lon, userId, preferences) =>
  API.post("/recommendations", { lat, lon, user_id: userId, preferences });
