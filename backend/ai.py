import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="StudyMate AI")

# Allow frontend to call the backend (important!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Change to your frontend URL later for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("OPENAI_API_KEY")

# Store conversation history (in memory - resets on restart)
messages = [
    {
        "role": "system",
        "content": "You are a smart study assistant. Give clear answers in simple English. Limit response to 5–8 lines."
    }
]

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(q: Question):
    if not API_KEY:
        return {"answer": "Error: OPENAI_API_KEY environment variable is not set."}

    # Add user question
    messages.append({"role": "user", "content": q.question})

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": messages,
        "temperature": 0.5,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()

        if "choices" in result:
            answer = result["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": answer})
            return {"answer": answer}
        else:
            return {"answer": "Error from OpenAI: " + str(result)}
    except Exception as e:
        return {"answer": f"Request failed: {str(e)}"}


# Optional: Health check route
@app.get("/")
async def root():
    return {"status": "StudyMate AI backend is running"}
