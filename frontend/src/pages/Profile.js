import React, { useState } from "react";

function Profile({ userEmail, onProfileSaved }) {
  const [userName, setUserName] = useState("");
  const [qualification, setQualification] = useState("");
  const [location, setLocation] = useState("");
  const [skills, setSkills] = useState("");
  const [socialCategory, setSocialCategory] = useState("");
  const [rural, setRural] = useState(false);
  const [pastInternships, setPastInternships] = useState(0);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Add checks for required fields as needed

    const profileData = {
      student_id: Date.now(), // Or use a better unique generator if needed
      email: userEmail,
      location_pref: location,
      name: userName,
      past_internships: Number(pastInternships),
      qualification: qualification,
      rural_background: Boolean(rural),
      skills: skills.split(",").map(s => s.trim()).filter(Boolean),
      social_category: socialCategory
    };

    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:5000/register_student", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profileData),
      });

      const data = await response.json();

      if (response.ok) {
        alert(data.message || "Student registered successfully!");
        if (onProfileSaved) onProfileSaved();
      } else {
        alert("Failed to save profile: " + (data.message || "Unknown error"));
      }
    } catch (error) {
      alert("Network error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: "50px auto", fontFamily: "Arial", padding: 20 }}>
      <h2 style={{ textAlign: "center" }}>Complete Your Profile</h2>
      <form onSubmit={handleSubmit}>
        <label>Full Name:</label>
        <input
          type="text"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />

        <label>Qualification:</label>
        <input
          type="text"
          value={qualification}
          onChange={(e) => setQualification(e.target.value)}
          placeholder="e.g. B.Tech IT"
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />

        <label>Preferred Location:</label>
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="e.g. Delhi"
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />

        <label>Past Internships:</label>
        <input
          type="number"
          value={pastInternships}
          min="0"
          onChange={(e) => setPastInternships(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        />

        <label>Rural Background?:</label>
        <select
          value={rural}
          onChange={(e) => setRural(e.target.value === "true")}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        >
          <option value={false}>No</option>
          <option value={true}>Yes</option>
        </select>

        <label>Social Category:</label>
        <select
          value={socialCategory}
          onChange={(e) => setSocialCategory(e.target.value)}
          required
          style={{ width: "100%", padding: 8, marginBottom: 12 }}
        >
          <option value="">Select</option>
          <option value="General">General</option>
          <option value="OBC">OBC</option>
          <option value="SC">SC</option>
          <option value="ST">ST</option>
        </select>

        <label>Skills (comma separated):</label>
        <input
          type="text"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          placeholder="e.g. Python, Excel"
          required
          style={{ width: "100%", padding: 8, marginBottom: 20 }}
        />

        <button
          type="submit"
          disabled={loading}
          style={{
            width: "100%",
            padding: 10,
            backgroundColor: "#28a745",
            color: "white",
            border: "none",
            cursor: loading ? "not-allowed" : "pointer"
          }}
        >
          {loading ? "Saving..." : "Save Profile"}
        </button>
      </form>
    </div>
  );
}

export default Profile;
