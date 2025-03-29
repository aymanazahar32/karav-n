// src/api.js
import axios from "axios";

const API_URL = "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Auth
export const signup = async (email, password) => {
  try {
    const response = await api.post("/signup", { email, password });
    return response;
  } catch (error) {
    throw error;
  }
};

export const login = async (email, password) => {
  try {
    const response = await api.post("/login", { email, password });
    return response;
  } catch (error) {
    throw error;
  }
};

// Preferences
export const updatePreferences = async (userId, preferences) => {
  try {
    const response = await api.post("/preferences", {
      user_id: userId,
      ...preferences,
    });
    return response;
  } catch (error) {
    throw error;
  }
};

// Reviews
export const postReview = async (userId, campsiteName, rating, reviewText) => {
  try {
    const response = await api.post("/review", {
      user_id: userId,
      campsite_name: campsiteName,
      rating,
      review_text: reviewText,
    });
    return response;
  } catch (error) {
    throw error;
  }
};

export const getReviews = async (campsiteName) => {
  try {
    const response = await api.get(`/reviews/${campsiteName}`);
    return response;
  } catch (error) {
    throw error;
  }
};

// Recommendations
export const getRecommendations = async (userId) => {
  try {
    // Get user's location using the browser's geolocation API
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject);
    });

    const response = await api.post("/recommendations", {
      user_id: userId,
      lat: position.coords.latitude,
      lon: position.coords.longitude,
    });
    return response;
  } catch (error) {
    throw error;
  }
};
