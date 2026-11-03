import os

from motor.motor_asyncio import AsyncIOMotorClient

# Configure this in the runtime environment. Prefer MONGO_URL; MONGO_URI is
# supported for compatibility with the existing Render configuration.
MONGO_URL = os.getenv("MONGO_URL") or os.getenv("MONGO_URI")
if not MONGO_URL:
    raise RuntimeError("Set MONGO_URL (or MONGO_URI) in the environment")

client = AsyncIOMotorClient(MONGO_URL)
db = client[os.getenv("MONGO_DB_NAME", "classroom_db")]
