from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, question, answer, voting

app = FastAPI()

# ✅ CORS (required for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ROUTES
app.include_router(auth.router, prefix="/api/auth")
app.include_router(question.router, prefix="/api/questions")
app.include_router(answer.router, prefix="/api/answers")
app.include_router(voting.router, prefix="/api/votes")


@app.get("/")
def home():
    return {"message": "API is running 🚀"}
