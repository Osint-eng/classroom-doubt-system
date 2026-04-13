from fastapi import APIRouter, HTTPException
from config.mongodb import db

router = APIRouter()

@router.post("/")
async def vote(data: dict):
    existing = await db.votes.find_one({
        "user": data["user"],
        "answer": data["answer"]
    })

    if existing:
        raise HTTPException(400, "Already voted")

    await db.votes.insert_one(data)

    await db.answers.update_one(
        {"_id": data["answer"]},
        {"$inc": {"votes": data["value"]}}
    )

    return {"message": "Vote recorded"}
