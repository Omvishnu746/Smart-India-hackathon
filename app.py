# app.py
import os
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Option A (direct - shared): full URI here
MONGO_URI = "mongodb+srv://Teamuser:Team1234@pm-cluster.ezvd3su.mongodb.net/pm_internship"

# Option B (env var) Uncomment & use .env for privacy
# MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["pm_internship"]

# --- ROUTES ---

@app.route("/students", methods=["GET"])
def get_students():
    """Fetch all students"""
    students = list(db["student"].find({}, {"_id": 0}))  # ✅ use 'student'
    return jsonify(students)

@app.route("/internships", methods=["GET"])
def get_internships():
    """Fetch all internships"""
    internships = list(db["internships"].find({}, {"_id": 0}))
    return jsonify(internships)

@app.route("/register_student", methods=["POST"])
def register_student():
    """Register a new student"""
    data = request.json
    if not data or "student_id" not in data:
        return {"error": "student_id missing"}, 400
    db["student"].insert_one(data)  # ✅ use 'student'
    return {"message": "Student added"}, 201

@app.route("/recommendations", methods=["GET"])
def recommendations():
    student_id = request.args.get("student_id")
    if not student_id:
        return {"error": "student_id query param required"}, 400

    # Try int match first, then string match, then id field fallback
    student = db["student"].find_one({"student_id": int(student_id)}, {"_id": 0}) \
              or db["student"].find_one({"student_id": student_id}, {"_id": 0}) \
              or db["student"].find_one({"id": int(student_id)}, {"_id": 0}) \
              or db["student"].find_one({"id": student_id}, {"_id": 0})

    if not student:
        return {"error": "student not found"}, 404

    candidates = list(db["internships"].find({}, {"_id": 0}))
    scored = []

    s_skills = set([k.lower() for k in student.get("skills", [])])

    for c in candidates:
        c_skills = set([k.lower() for k in c.get("skills_required", [])])
        match = len(s_skills & c_skills)
        scored.append({"internship": c, "score": match})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(scored[:10])


# --- MAIN ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)
