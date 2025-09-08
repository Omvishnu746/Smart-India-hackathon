from pymongo import MongoClient

MONGO_URI = "mongodb+srv://Teamuser:Team1234@pm-cluster.ezvd3su.mongodb.net/pm_internship"
client = MongoClient(MONGO_URI)
db = client["pm_internship"]

students = list(db["student"].find({}))
for i, student in enumerate(students, start=1):
    db["student"].update_one(
        {"_id": student["_id"]},
        {"$set": {"student_id": i}}
    )

print(" student_id fields added to all students.")
