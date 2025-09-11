import React from "react";

function Navbar({ onNavigate }) {
  const navStyle = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    backgroundColor: "#0052cc",
    padding: "10px 20px",
    color: "white",
    position: "fixed",
    top: 0,
    width: "100%",
    zIndex: 1000,
  };

  const linkStyle = {
    color: "white",
    marginLeft: 20,
    background: "none",
    border: "none",
    cursor: "pointer",
    fontWeight: "bold",
    fontSize: "1rem",
  };

  return (
    <nav style={navStyle}>
      <div style={{ fontWeight: "bold", fontSize: 18 }}>PM Internship Scheme</div>
      <div>
        <button style={linkStyle} onClick={() => onNavigate("registration")}>
          Registration
        </button>
        <button style={linkStyle} onClick={() => onNavigate("login")}>
          Login
        </button>
        <button style={linkStyle} onClick={() => onNavigate("opportunities")}>
          Opportunities ▼
        </button>
      </div>
    </nav>
  );
}

export default Navbar;
