// src/components/SignupForm.js
import React, { useState } from "react";
import { signup } from "../api";

function SignupForm({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await signup(email, password);
      if (res.data.user) {
        setUser(res.data.user);
      }
    } catch (err) {
      alert("Signup failed: " + err.response?.data?.error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Sign Up</h2>
      <div>
        <label>Email: </label>
        <input
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          type="email"
        />
      </div>
      <div>
        <label>Password: </label>
        <input
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          type="password"
        />
      </div>
      <button type="submit">Sign Up</button>
    </form>
  );
}

export default SignupForm;
