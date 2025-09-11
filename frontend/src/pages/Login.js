import React, { useState } from "react";
import studentsData from "../data/Student.json";

function Login({ onLoginClick, onSwitchToSignup }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    const user = studentsData.find(
      (student) => student.email.toLowerCase() === email.toLowerCase()
    );

    if (!user) {
      setError("User not found. Please register.");
      return;
    }
    if (user.password !== password) {
      setError("Incorrect password.");
      return;
    }
    // Login success
    onLoginClick(user.email);
  };

  return (
    <div style={{ maxWidth: 400, margin: "50px auto", fontFamily: "Arial", padding: 20 }}>
      <h2>Login</h2>
      {error && <div style={{ color: "red", marginBottom: 10 }}>{error}</div>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />
        <button
          type="submit"
          style={{
            width: "100%",
            padding: 10,
            backgroundColor: "#007bff",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Login
        </button>
      </form>
      <p style={{ marginTop: 10 }}>
        New user?{" "}
        <button onClick={onSwitchToSignup} style={{ color: "blue", cursor: "pointer", background: "none", border: "none", padding: 0 }}>
          Register here
        </button>
      </p>
    </div>
  );
}

export default Login;
