// src/components/LoginForm.js
import React, { useState } from "react";
import { login } from "../api";

function LoginForm({ setUser }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await login(email, password);
      if (res.data.user) {
        setUser(res.data.user);
      }
    } catch (err) {
      alert("Login failed: " + err.response?.data?.error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Log In</h2>
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
      <button type="submit">Log In</button>
    </form>
  );
}

export default LoginForm;
