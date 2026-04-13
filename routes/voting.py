from fastapi import APIRouter, HTTPException
from config.mongodb import db
from bson import ObjectId

router = APIRouter()

# ✅ VOTE
@router.post("/")
async def vote(data: dict):
    try:
        existing = await db.votes.find_one({
            "user": data["user"],
            "answer": data["answer"]
        })

        if existing:
            raise HTTPException(status_code=400, detail="Already voted")

        await db.votes.insert_one(data)

        await db.answers.update_one(
            {"_id": ObjectId(data["answer"])},  # 🔥 important fix
            {"$inc": {"votes": data["value"]}}
        )

        return {"message": "Vote recorded"}
    except Exception as e:
        return {"error": str(e)}
