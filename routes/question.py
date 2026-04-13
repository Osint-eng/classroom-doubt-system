from fastapi import APIRouter
from config.mongodb import db
from datetime import datetime

router = APIRouter()

# ✅ CREATE QUESTION
@router.post("/")
async def create_question(question: dict):
    try:
        question["createdAt"] = datetime.utcnow()
        question["votes"] = 0

        result = await db.questions.insert_one(question)

        return {"id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}


# ✅ GET QUESTIONS
@router.get("/")
async def get_questions():
    try:
        questions = []

        async for q in db.questions.find():
            q["_id"] = str(q["_id"])  # 🔥 important
            questions.append(q)

        return questions
    except Exception as e:
        return {"error": str(e)}
