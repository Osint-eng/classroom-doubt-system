from fastapi import APIRouter, HTTPException
from config.mongodb import db
from utils.hash import hash_password, verify_password
from utils.jwt import create_token
from schemas.user_schema import UserCreate, UserLogin

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(400, "User already exists")

    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["reputation"] = 0

    result = await db.users.insert_one(user_dict)

    token = create_token({"id": str(result.inserted_id)})
    return {"token": token}


@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({"id": str(db_user["_id"])})
    return {"token": token}
