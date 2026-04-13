# config/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
import os

# 🔥 Replace this with your MongoDB Atlas URL
MONGO_URL = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# ✅ Create client
client = AsyncIOMotorClient(MONGO_URL)

# ✅ Create database
db = client["classroom_db"]  # you can name anything
