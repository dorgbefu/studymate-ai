import requests
import os

API_KEY = os.getenv("OPENAI_API_KEY")

def ask_ai(question: str):
    if not API_KEY:
        return "Error: OPENAI_API_KEY not set."

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a smart study assistant. Give clear answers in simple English. Limit response to 5–8 lines."
            },
            {"role": "user", "content": question}
        ],
        "temperature": 0.5,
        "max_tokens": 300
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return str(result)
