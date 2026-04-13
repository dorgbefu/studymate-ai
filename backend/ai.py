import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Create the FastAPI app
app = FastAPI(title="StudyMate AI")

# Enable CORS so your frontend can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")

# Conversation history
messages = [
    {
        "role": "system",
        "content": "You are a smart study assistant. Give clear answers in simple English. Limit response to 5–8 lines."
    }
]

class Question(BaseModel):
    question: str

# This is the endpoint your frontend is calling
@app.post("/ask")
async def ask_question(q: Question):
    if not API_KEY:
        return {"answer": "Error: OPENAI_API_KEY is not set in Environment Variables."}

    # Add user question to history
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
            return {"answer": "OpenAI error: " + str(result)}
    except Exception as e:
        return {"answer": f"Failed to get response: {str(e)}"}


# Health check route
@app.get("/")
async def root():
    return {"status": "StudyMate AI backend is running ✅"}
