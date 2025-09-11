import React, { useState } from "react";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Profile from "./pages/Profile";
import Recommendations from "./pages/Recommendations";
import Navbar from "./components/Navbar";
import studentsData from "./data/Student.json";

function App() {
  const [userEmail, setUserEmail] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [currentPage, setCurrentPage] = useState("login"); // "login" | "signup" | "profile" | "recommendations"

  const handleNavigate = (page) => {
    if (page === "registration") {
      setCurrentPage("signup");
    } else if (page === "login") {
      setCurrentPage("login");
    } else if (page === "opportunities") {
      if (userProfile) {
        setCurrentPage("recommendations");
      } else {
        setCurrentPage("login");
      }
    }
  };

  const handleLoginClick = (email) => {
    setUserEmail(email);
    const profile = studentsData.find(
      (student) => student.email.toLowerCase() === email.toLowerCase()
    );
    setUserProfile(profile || null);

    if (profile) {
      setCurrentPage("recommendations"); // skip profile if exists
    } else {
      setCurrentPage("profile"); // show profile form if no profile
    }
  };

  const handleSignupClick = (email) => {
    setUserEmail(email);
    setUserProfile(null);
    setCurrentPage("profile");
  };

  const handleProfileSaved = () => {
    // For now, simulate that profile is saved
    setCurrentPage("recommendations");
  };

  return (
    <>
      <Navbar onNavigate={handleNavigate} />
      <div style={{ marginTop: 60, padding: 20 }}>
        {!userEmail && currentPage === "login" && (
          <Login onLoginClick={handleLoginClick} onSwitchToSignup={() => setCurrentPage("signup")} />
        )}
        {!userEmail && currentPage === "signup" && (
          <Signup onSignupClick={handleSignupClick} onSwitchToLogin={() => setCurrentPage("login")} />
        )}
        {userEmail && !userProfile && currentPage === "profile" && (
          <Profile userEmail={userEmail} onProfileSaved={handleProfileSaved} />
        )}
        {userEmail && userProfile && currentPage === "recommendations" && (
          <Recommendations userEmail={userEmail} />
        )}
      </div>
    </>
  );
}

export default App;
