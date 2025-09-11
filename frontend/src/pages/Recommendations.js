import React from "react";
import internshipsData from "../data/Internships.json";
import studentsData from "../data/Student.json";

function Recommendations({ userEmail }) {
  // Find logged-in user profile from Student.json
  const userProfile = studentsData.find(
    (student) => student.email.toLowerCase() === userEmail.toLowerCase()
  );

  // Filter internships for user's skills as a demonstration
  let filteredInternships = internshipsData;
  if (userProfile) {
    filteredInternships = internshipsData.filter((internship) =>
      internship.skills_required.some((skill) =>
        userProfile.skills.map((s) => s.toLowerCase()).includes(skill.toLowerCase())
      )
    );
  }

  return (
    <div style={{ maxWidth: 600, margin: "30px auto", fontFamily: "Arial", padding: 20 }}>
      <h2>
        Recommended Internships for {userEmail}
      </h2>
      {filteredInternships.length === 0 && (
        <div>No personalized matches found. Showing all internships:</div>
      )}
      {(filteredInternships.length ? filteredInternships : internshipsData).map((internship) => (
        <div
          key={internship._id}
          style={{
            border: "1px solid #ccc",
            borderRadius: 8,
            padding: 15,
            marginBottom: 15,
            boxShadow: "0 2px 8px #eee",
          }}
        >
          <h3>{internship.title}</h3>
          <p><strong>Company:</strong> {internship.company}</p>
          <p><strong>Location:</strong> {internship.location}</p>
          <p><em>Skills Required:</em> {internship.skills_required.join(", ")}</p>
          <p><em>Sector:</em> {internship.sector}</p>
          {userProfile && (
            <p>
              <em>
                Match:{" "}
                {internship.skills_required
                  .filter((skill) =>
                    userProfile.skills.map((s) => s.toLowerCase()).includes(skill.toLowerCase())
                  )
                  .join(", ") || "No skill match"}
              </em>
            </p>
          )}
          <button
            style={{ marginRight: 10, padding: "8px 12px" }}
            onClick={() => alert(`Applied to ${internship.title}`)}
          >
            Apply
          </button>
          <button
            style={{ padding: "8px 12px" }}
            onClick={() => alert(`Saved ${internship.title} for later`)}
          >
            Save
          </button>
        </div>
      ))}
    </div>
  );
}

export default Recommendations;
