import requests
from datetime import datetime
import os

# === PUT YOUR OPENAI API KEY HERE ===
OPENAI_API_KEY = "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
"   # ← Change this

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Direct fast answers
    if "today" in q and ("date" in q or "day" in q):
        return f"**Today's Date:**\n{datetime.now().strftime('%A, %B %d, %Y')}"
    
    if "president of ghana" in q or "ghana president" in q:
        return "**President of Ghana:** John Dramani Mahama (since January 7, 2025)"
    
    if "japan" in q and ("prime" in q or "president" in q):
        return "**Prime Minister of Japan:** Sanae Takaichi (since October 21, 2025)"
    
    # Use GPT for everything else
    return ask_gpt(question)


def ask_gpt(question: str) -> str:
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",   # cheap & good
            "messages": [
                {"role": "system", "content": "You are a helpful study assistant. Answer clearly and accurately for students."},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 400
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=15)
        
        if response.status_code == 200:
            answer = response.json()["choices"][0]["message"]["content"]
            return answer.strip()
        else:
            return f"API Error ({response.status_code}). Check your API key."
            
    except Exception as e:
        return f"Error connecting to GPT: {str(e)[:100]}"


# For testing locally
if __name__ == "__main__":
    print(ask_ai("what is matter"))
    print(ask_ai("who is the president of ghana"))
    print(ask_ai("what is orange"))
