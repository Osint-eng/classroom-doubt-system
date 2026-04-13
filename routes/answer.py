from fastapi import APIRouter
from config.mongodb import db
from datetime import datetime

router = APIRouter()

@router.post("/")
async def add_answer(answer: dict):
    answer["createdAt"] = datetime.utcnow()
    answer["votes"] = 0

    result = await db.answers.insert_one(answer)
    return {"id": str(result.inserted_id)}


@router.get("/{question_id}")
async def get_answers(question_id: str):
    answers = []
    async for a in db.answers.find({"questionId": question_id}):
        a["_id"] = str(a["_id"])
        answers.append(a)
    return answers
