from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb+srv://varshithpediredla_db_user:0JmImRhR3gsBK6HX@cluster0.bcdekbb.mongodb.net/classroom_db?retryWrites=true&w=majority"

client = AsyncIOMotorClient(MONGO_URL)

db = client["classroom_db"]
