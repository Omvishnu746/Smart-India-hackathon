import React, { useState } from "react";

function Signup({ onSignupClick, onSwitchToLogin }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !email || !password || !confirmPassword) {
      alert("Please fill all fields");
      return;
    }
    if (password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    alert(`Signed up with:
      Name: ${name}
      Email: ${email}`);
    if (onSignupClick) onSignupClick(email);
  };

  return (
    <div style={{ maxWidth: 400, margin: "50px auto", fontFamily: "Arial", padding: 20 }}>
      <h2 style={{ textAlign: "center" }}>Signup</h2>
      <form onSubmit={handleSubmit}>
        <label>Full Name:</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />
        <label>Confirm Password:</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 20 }}
        />
        <button
          type="submit"
          style={{ width: "100%", padding: 10, backgroundColor: "#28a745", color: "white", border: "none", cursor: "pointer" }}
        >
          Signup
        </button>
      </form>
      <p style={{ textAlign: "center", marginTop: 15 }}>
        Already have an account?{" "}
        <button
          onClick={onSwitchToLogin}
          style={{ color: "#007BFF", background: "none", border: "none", cursor: "pointer" }}
        >
          Login
        </button>
      </p>
    </div>
  );
}

export default Signup;
