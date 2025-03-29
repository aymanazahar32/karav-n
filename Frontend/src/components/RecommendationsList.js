import React, { useState, useEffect } from "react";
import { getRecommendations } from "../api";

function RecommendationsList({ user }) {
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [aiSummary, setAiSummary] = useState("");

  useEffect(() => {
    fetchRecommendations();
  }, [user]);

  const fetchRecommendations = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await getRecommendations(user.id);
      setRecommendations(response.data.results);
      setAiSummary(response.data.ai_summary);
    } catch (err) {
      if (err.message === "User denied geolocation") {
        setError("Please enable location access to get personalized recommendations.");
      } else {
        setError("Failed to load recommendations. Please try again later.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="recommendations-container">
        <div className="loading-spinner">Loading recommendations...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="recommendations-container">
        <div className="error-message">{error}</div>
        <button onClick={fetchRecommendations} className="retry-button">
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="recommendations-container">
      <h2>Your Personalized Camping Spots</h2>
      {aiSummary && (
        <div className="ai-summary">
          <h3>AI Recommendation</h3>
          <p>{aiSummary}</p>
        </div>
      )}
      <div className="recommendations-grid">
        {recommendations.map((spot, index) => (
          <div key={index} className="recommendation-card">
            <div className="card-image">
              <img 
                src={`https://source.unsplash.com/random/800x600/?camping,${spot.name}`} 
                alt={spot.name} 
              />
            </div>
            <div className="card-content">
              <h3>{spot.name}</h3>
              <p className="location">
                Distance: {spot.distance.toFixed(1)} km
              </p>
              <div className="features">
                <span className="feature-tag">
                  Light Pollution: {spot.light_pollution_level}/10
                </span>
                <span className="feature-tag">
                  Weather: {spot.weather.condition}
                </span>
                <span className="feature-tag">
                  {spot.availability ? "Available" : "Not Available"}
                </span>
              </div>
              <div className="card-footer">
                <div className="rating">
                  <span className="score">Score: {spot.score.toFixed(1)}</span>
                </div>
                <button className="view-details">View Details</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecommendationsList; 