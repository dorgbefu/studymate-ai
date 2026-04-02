from fastapi import FastAPI
from pydantic import BaseModel
from ai import ask_ai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.get("/")
def home():
    return {"message": "StudyMate AI API is running"}

@app.post("/ask")
def ask(question: Question):
    answer = ask_ai(question.question)
    return {"answer": answer}
