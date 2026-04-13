from fastapi import APIRouter
from config.mongodb import db
from datetime import datetime

router = APIRouter()

# ✅ ADD ANSWER
@router.post("/")
async def add_answer(answer: dict):
    try:
        answer["createdAt"] = datetime.utcnow()
        answer["votes"] = 0

        result = await db.answers.insert_one(answer)

        return {"id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e)}


# ✅ GET ANSWERS
@router.get("/{question_id}")
async def get_answers(question_id: str):
    try:
        answers = []

        async for a in db.answers.find({"questionId": question_id}):
            a["_id"] = str(a["_id"])  # 🔥 important
            answers.append(a)

        return answers
    except Exception as e:
        return {"error": str(e)}
