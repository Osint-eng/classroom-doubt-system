from fastapi import FastAPI
from routes import auth, question, answer, voting

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth")
app.include_router(question.router, prefix="/api/questions")
app.include_router(answer.router, prefix="/api/answers")
app.include_router(voting.router, prefix="/api/votes")
