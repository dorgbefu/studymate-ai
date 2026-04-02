from fastapi import FastAPI
from pydantic import BaseModel
from backend.ai import ask_ai

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "StudyMate AI API is running"}

@app.post("/ask")
def ask(question: Question):
    answer = ask_ai(question.question)
    return {"answer": answer}