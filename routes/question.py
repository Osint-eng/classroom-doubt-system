from fastapi import APIRouter, Depends
from config.mongodb import db
from datetime import datetime

router = APIRouter()

@router.post("/")
async def create_question(question: dict):
    question["createdAt"] = datetime.utcnow()
    question["votes"] = 0

    result = await db.questions.insert_one(question)
    return {"id": str(result.inserted_id)}


@router.get("/")
async def get_questions():
    questions = []
    async for q in db.questions.find():
        q["_id"] = str(q["_id"])
        questions.append(q)
    return questions
