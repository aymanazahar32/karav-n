// src/components/Dashboard.js
import React, { useState } from "react";
import RecommendationsList from "./RecommendationsList";
import Profile from "./Profile";

function Dashboard({ user, setUser }) {
  const [view, setView] = useState("recommendations");

  const handleLogout = () => {
    setUser(null);
  };

  return (
    <div>
      <div>
        <button onClick={() => setView("recommendations")}>Recommendations</button>
        <button onClick={() => setView("profile")}>Profile</button>
        <button onClick={handleLogout}>Logout</button>
      </div>

      {view === "recommendations" && <RecommendationsList user={user} />}
      {view === "profile" && <Profile user={user} />}
    </div>
  );
}

export default Dashboard;
