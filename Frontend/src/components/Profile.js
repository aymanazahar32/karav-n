// src/components/Profile.js
import React, { useState } from "react";
import { updatePreferences } from "../api";

function Profile({ user }) {
  const [fishing, setFishing] = useState(user.prefers_fishing);
  const [hiking, setHiking] = useState(user.prefers_hiking);
  const [solitude, setSolitude] = useState(user.prefers_solitude);
  const [message, setMessage] = useState("");

  const savePreferences = async () => {
    try {
      const res = await updatePreferences(user.id, {
        prefers_fishing: fishing,
        prefers_hiking: hiking,
        prefers_solitude: solitude
      });
      setMessage("Preferences updated.");
    } catch (err) {
      setMessage("Error updating preferences.");
    }
  };

  return (
    <div>
      <h2>Profile</h2>
      <p>User: {user.email}</p>
      <div>
        <label>
          <input
            type="checkbox"
            checked={fishing}
            onChange={(e) => setFishing(e.target.checked)}
          />
          Prefers Fishing
        </label>
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={hiking}
            onChange={(e) => setHiking(e.target.checked)}
          />
          Prefers Hiking
        </label>
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={solitude}
            onChange={(e) => setSolitude(e.target.checked)}
          />
          Prefers Solitude
        </label>
      </div>
      <button onClick={savePreferences}>Save Preferences</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default Profile;
