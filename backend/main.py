from fastapi import FastAPI
from ai import ask_ai
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(question: Question):
    answer = ask_ai(question.question)
    return {"answer": answer}