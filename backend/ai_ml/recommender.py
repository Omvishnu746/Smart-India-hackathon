import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Recommender:
    def __init__(self, students_file, internships_file):
        # Load student data
        with open(students_file, "r") as f:
            self.students = json.load(f)

        # Load internship data
        with open(internships_file, "r") as f:
            self.internships = json.load(f)

    def load_from_db(self, db):
        """Load from MongoDB if available, else keep JSON data"""
        students = list(db["student"].find({}, {"_id": 0}))
        internships = list(db["internships"].find({}, {"_id": 0}))
        if students:
            self.students = students
        if internships:
            self.internships = internships

    def rule_based(self, student_id):
        """Simple rule: match student skills with internship requirements"""
        student = next((s for s in self.students if s.get("student_id") == student_id), None)
        if not student:
            return []

        s_skills = set([skill.lower() for skill in student.get("skills", [])])
        scored = []

        for internship in self.internships:
            i_skills = set([skill.lower() for skill in internship.get("skills_required", [])])
            match = len(s_skills & i_skills)
            scored.append({"internship": internship, "score": match})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:10]

    def ml_based(self, student_id):
        """Content-based filtering with cosine similarity"""
        student = next((s for s in self.students if s.get("student_id") == student_id), None)
        if not student:
            return []

        student_text = " ".join(student.get("skills", []))
        internship_texts = [" ".join(i.get("skills_required", [])) for i in self.internships]

        vectorizer = CountVectorizer().fit([student_text] + internship_texts)
        vectors = vectorizer.transform([student_text] + internship_texts)
        similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

        scored = [{"internship": i, "score": float(sim)} for i, sim in zip(self.internships, similarities)]
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:10]
