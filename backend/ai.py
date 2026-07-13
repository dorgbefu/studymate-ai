import requests
from datetime import datetime
import os

# Get API key from Render environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ask_ai(question: str) -> str:
    if not OPENAI_API_KEY or len(OPENAI_API_KEY) < 20:
        return f"API Key not loaded properly. Length = {len(OPENAI_API_KEY) if OPENAI_API_KEY else 0}"
   
    q = question.lower().strip()
   
    # Direct fast answers
    if "today" in q and ("date" in q or "day" in q):
        return f"**Today's Date:**\n{datetime.now().strftime('%A, %B %d, %Y')}"
   
    if "president of ghana" in q or "ghana president" in q:
        return "**President of Ghana:** John Dramani Mahama (since January 7, 2025)"
   
    if "japan" in q and ("prime minister" in q or "president" in q):
        return "**Prime Minister of Japan:** Sanae Takaichi (since October 21, 2025)"
   
    # Use GPT for all other questions
    return ask_gpt(question)


def ask_gpt(question: str) -> str:
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": """You are StudyMate AI, a helpful and up-to-date study assistant for students.

Core rules:
- Always try to provide the most current and accurate information possible.
- For recent events (2024, 2025, 2026), provide latest available information.
- Do NOT mention your knowledge cutoff, training date, or any internal limitations.
- If asked about your training or how you work, politely say: "I'm sorry, I can't share details about my internal workings."
- Keep answers clear, educational, and student-friendly."""
                },
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 600
        }
       
        response = requests.post(url, headers=headers, json=payload, timeout=15)
       
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"OpenAI API Error: {response.status_code}"
           
    except Exception as e:
        return f"Connection error: {str(e)[:100]}"


# Test
if __name__ == "__main__":
    print(ask_ai("what is matter"))
    print(ask_ai("hi"))
