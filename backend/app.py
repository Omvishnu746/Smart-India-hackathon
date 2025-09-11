from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from ai_ml.advanced_recommender import AdvancedRecommender

# Flask app
app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGO_URI = "mongodb+srv://Teamuser:Team1234@pm-cluster.ezvd3su.mongodb.net/pm_internship"
client = MongoClient(MONGO_URI)
db = client["pm_internship"]

# Initialize recommender globally
recommender = AdvancedRecommender(db=db)

# ----------------- ROUTES -----------------

@app.route("/recommendations", methods=["GET"])
def recommendations():
    student_id = request.args.get("student_id", type=int)
    top_n = request.args.get("top_n", default=5, type=int)

    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    err, recs = recommender.recommend(student_id, top_n=top_n)
    if err:
        return jsonify(err), 404
    return jsonify(recs), 200


# --- Students ---
@app.route("/students", methods=["GET"])
def get_students():
    students = list(db["Student"].find({}, {"_id": 0}))
    return jsonify(students)


@app.route("/register_student", methods=["POST"])
def register_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid student data"}), 400
    db["Student"].insert_one(data)
    recommender.load_from_db(db)  # refresh recommender
    return jsonify({"message": "Student registered successfully"}), 201


# --- Internships ---
@app.route("/internships", methods=["GET"])
def get_internships():
    internships = list(db["internships"].find({}, {"_id": 0}))
    return jsonify(internships)


@app.route("/register_internship", methods=["POST"])
def register_internship():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid internship data"}), 400
    db["internships"].insert_one(data)
    recommender.load_from_db(db)  # refresh recommender
    return jsonify({"message": "Internship registered successfully"}), 201


# --- Recommendations ---
@app.route("/recommend_internships", methods=["GET"])
def recommend_internships():
    student_id = request.args.get("student_id")
    if not student_id:
        return jsonify({"error": "Missing student_id"}), 400

    try:
        student_id = int(student_id)
    except ValueError:
        return jsonify({"error": "student_id must be integer"}), 400

    err, recs = recommender.recommend(student_id, top_n=5)
    if err:
        return jsonify(err), 404
    return jsonify(recs)


# --- Skill Gap + Course Recommendation ---
@app.route("/recommend_courses", methods=["GET"])
def recommend_courses():
    student_id = request.args.get("student_id")
    internship_id = request.args.get("internship_id")

    if not student_id or not internship_id:
        return jsonify({"error": "Missing student_id or internship_id"}), 400

    try:
        student_id = int(student_id)
        internship_id = int(internship_id)
    except ValueError:
        return jsonify({"error": "IDs must be integers"}), 400

    gap_info = recommender.skill_gap(student_id, internship_id)
    if "error" in gap_info:
        return jsonify(gap_info), 404

    courses = recommender.recommend_courses_for_skills(gap_info["missing_skills"], top_k=5)

    return jsonify({
        "skill_gap": gap_info,
        "recommended_courses": courses
    })
    
# ---------- SKILL GAP + COURSE RECOMMENDATION ----------
@app.route("/skill_gap", methods=["GET"])
def skill_gap():
    """
    Example:
    /skill_gap?student_id=1&internship_id=201

    Returns:
    {
      "student_id": 1,
      "internship_id": 201,
      "missing_skills": ["Machine Learning"],
      "have_skills": ["Python"],
      "recommended_courses": [
         {
           "course": { "course_id": "c101", "title": "Intro to ML", ... },
           "score": 100.0,
           "matched_tags": ["machine learning"]
         }
      ]
    }
    """
    student_id = request.args.get("student_id", type=int)
    internship_id = request.args.get("internship_id", type=int)

    if not student_id or not internship_id:
        return jsonify({"error": "student_id and internship_id required"}), 400

    gap_info = recommender.skill_gap(student_id, internship_id)

    # If missing skills exist, recommend courses
    if "missing_skills" in gap_info and gap_info["missing_skills"]:
        courses = recommender.recommend_courses_for_skills(gap_info["missing_skills"])
        # convert score to percentage
        for c in courses:
            c["score"] = round(c["score"] * 100, 2)
        gap_info["recommended_courses"] = courses
    else:
        gap_info["recommended_courses"] = []

    return jsonify(gap_info), 200



# --- Analytics ---
@app.route("/analytics", methods=["GET"])
def analytics():
    return jsonify(recommender.analytics())


# ----------------- MAIN -----------------
if __name__ == "__main__":
    app.run(debug=True)
