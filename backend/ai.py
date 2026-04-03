import requests
import os

API_KEY = os.getenv("OPENAI_API_KEY")

# Store conversation history
messages = [
    {
        "role": "system",
        "content": "You are a smart study assistant. Give clear answers in simple English. Limit response to 5–8 lines."
    }
]

def ask_ai(question: str):
    if not API_KEY:
        return "Error: OPENAI_API_KEY not set."

    # Add user question to conversation
    messages.append({"role": "user", "content": question})

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

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        answer = result["choices"][0]["message"]["content"]

        # Save AI response to conversation
        messages.append({"role": "assistant", "content": answer})

        return answer
    else:
        return str(result)
