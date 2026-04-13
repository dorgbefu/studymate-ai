from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

app = FastAPI(title="StudyMate AI")

# Allow your frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are a smart study assistant. Give clear answers in simple English. Limit response to 5–8 lines."}
]

class Question(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(q: Question):
    if not API_KEY:
        return {"answer": "Error: OPENAI_API_KEY is not set in Environment Variables on Render."}

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
            return {"answer": "OpenAI API error: " + str(result)}
    except Exception as e:
        return {"answer": f"Request failed: {str(e)}"}


@app.get("/")
async def root():
    return {"status": "StudyMate AI is running ✅", "model": "gpt-4o-mini"}
