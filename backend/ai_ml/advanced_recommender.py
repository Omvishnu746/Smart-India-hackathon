import json
import math
import traceback
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Helper
def _norm(s):
    return s.strip().lower() if isinstance(s, str) else ""

def _to_text_for_tfidf(doc):
    parts = []
    if "skills" in doc:
        parts.append(" ".join(doc["skills"]))
    if "skills_required" in doc:
        parts.append(" ".join(doc["skills_required"]))
    for k in ("qualification", "title", "company", "location"):
        if k in doc and doc[k]:
            parts.append(str(doc[k]))
    return " ".join(parts)


class AdvancedRecommender:
    def __init__(self, db=None, students_file="data/Student.json",
                 internships_file="data/internships.json", courses_file="data/courses.json",
                 policies_file="data/policies.json"):
        # Fallback
        self.students, self.internships, self.courses, self.policies = [], [], [], []
        self.db = db
        if db is not None:
            self.load_from_db(db)

        self._vectorizer = None
        self._internship_texts = None
        self._internship_vectors = None

    # ---------- DB Loader ----------
    def load_from_db(self, db):
        try:
            self.students = list(db["Student"].find({}, {"_id": 0}))
            self.internships = list(db["internships"].find({}, {"_id": 0}))
            self.courses = list(db["courses"].find({}, {"_id": 0}))
            self.policies = list(db["policies"].find({}, {"_id": 0}))
            return True
        except Exception as e:
            print("DB load error:", e)
            return False

    # ---------- TF-IDF ----------
    def _ensure_vectors(self):
        if self._vectorizer is not None:
            return
        self._internship_texts = [_to_text_for_tfidf(i) for i in self.internships]
        self._vectorizer = TfidfVectorizer()
        if self._internship_texts:
            self._internship_vectors = self._vectorizer.fit_transform(self._internship_texts)

    # ---------- Scoring ----------
    def score_internship_for_student(self, student, internship, weights=None):
        if weights is None:
            weights = {"skill_match": 0.5, "tfidf": 0.25, "location": 0.1, "qualification": 0.1, "fresh_bonus": 0.05}

        s_skills = set([_norm(s) for s in student.get("skills", [])])
        i_skills = set([_norm(s) for s in internship.get("skills_required", [])])

        inter = s_skills & i_skills
        skill_count_norm = (len(inter) / max(1, len(i_skills)))

        self._ensure_vectors()
        tfidf_sim = 0.0
        try:
            if self._internship_vectors is not None:
                stu_vec = self._vectorizer.transform([_to_text_for_tfidf(student)])
                sims = cosine_similarity(stu_vec, self._internship_vectors).flatten()
                idx = self._internship_texts.index(_to_text_for_tfidf(internship))
                tfidf_sim = float(sims[idx])
        except:
            pass

        location_score = 1.0 if _norm(student.get("location_pref")) == _norm(internship.get("location")) else 0.0
        qualification_score = 1.0 if _norm(student.get("qualification", "")) in str(internship.get("allowed_qualifications", "")).lower() else 0.5
        fresh_bonus = 0.5 if student.get("past_internships", 0) == 0 else 0.0

        final_score = (
            weights["skill_match"] * skill_count_norm +
            weights["tfidf"] * tfidf_sim +
            weights["location"] * location_score +
            weights["qualification"] * qualification_score +
            weights["fresh_bonus"] * fresh_bonus
        )

        return round(final_score * 100, 2), {  # percentage
            "skill_match": skill_count_norm,
            "tfidf_sim": tfidf_sim,
            "location_score": location_score,
            "qualification_score": qualification_score,
            "fresh_bonus": fresh_bonus
        }

    # ---------- Recommendation ----------
    def recommend(self, student_id, top_n=5):
        student = next((s for s in self.students if s.get("student_id") == student_id), None)
        if not student:
            return {"error": "student not found"}, []

        scored = []
        for i in self.internships:
            score, explain = self.score_internship_for_student(student, i)
            scored.append({"internship": i, "score": score, "explain": explain})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return None, scored[:top_n]

    # ---------- Skill Gap ----------
    def skill_gap(self, student_id, internship_id):
        student = next((s for s in self.students if s.get("student_id") == student_id), None)
        internship = next((i for i in self.internships if i.get("internship_id") == internship_id), None)
        if not student or not internship:
            return {"error": "student/internship not found"}

        s_skills = set([_norm(x) for x in student.get("skills", [])])
        i_skills = set([_norm(x) for x in internship.get("skills_required", [])])
        missing = sorted(list(i_skills - s_skills))

        return {"student_id": student_id, "internship_id": internship_id, "missing_skills": missing, "have_skills": list(s_skills & i_skills)}

    # ---------- Courses ----------
    def recommend_courses_for_skills(self, missing_skills, top_k=5):
        scored = []
        if not missing_skills:
            return scored
        missing_set = set([_norm(x) for x in missing_skills])
        for c in self.courses:
            tags = set([_norm(t) for t in c.get("tags", [])] + [_norm(t) for t in c.get("skills", [])])
            overlap = missing_set & tags
            if overlap:
                score = len(overlap) / len(missing_set)
                scored.append({"course": c, "score": round(score * 100, 2), "matched_tags": list(overlap)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    # ---------- Analytics ----------
    def analytics(self):
        skill_freq = defaultdict(int)
        for i in self.internships:
            for s in i.get("skills_required", []):
                skill_freq[_norm(s)] += 1
        return {"num_students": len(self.students), "num_internships": len(self.internships), "num_courses": len(self.courses), "top_skills": sorted(skill_freq.items(), key=lambda x: x[1], reverse=True)[:10]}
