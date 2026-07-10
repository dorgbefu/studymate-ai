import requests
from datetime import datetime
import os

# Get API key from environment variable (secure)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    # Fallback message if key is missing
    def ask_ai(question: str):
        return "⚠️ API key not configured. Please set OPENAI_API_KEY in your Render environment variables."
else:
    def ask_ai(question: str) -> str:
        q = question.lower().strip()
        
        # Direct answers (fast, no cost)
        if "today" in q and ("date" in q or "day" in q):
            return f"**Today's Date:**\n{datetime.now().strftime('%A, %B %d, %Y')}"
        
        if "president of ghana" in q or "ghana president" in q:
            return "**President of Ghana:** John Dramani Mahama (since January 7, 2025)"
        
        if "japan" in q and ("prime minister" in q or "president" in q):
            return "**Prime Minister of Japan:** Sanae Takaichi (since October 21, 2025)"
        
        # Use GPT
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
                {"role": "system", "content": "You are a helpful and accurate study assistant for students."},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"OpenAI API Error: {response.status_code}"
            
    except Exception as e:
        return f"Connection error: {str(e)[:80]}"


# Test
if __name__ == "__main__":
    print(ask_ai("what is matter"))
