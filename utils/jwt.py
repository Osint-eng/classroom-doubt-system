from jose import jwt
from datetime import datetime, timedelta
import os

SECRET = os.getenv("JWT_SECRET")

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm="HS256")
