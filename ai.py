import requests
import os
from bs4 import BeautifulSoup

API_KEY = os.getenv("OPENAI_API_KEY")

def ask_ai(question: str) -> str:
    if not API_KEY:
        return "❌ Error: OPENAI_API_KEY is not set in Render Environment Variables."

    # Decide whether to search the web
    if should_search_web(question):
        search_result = web_search(question)
        # Combine search result with AI for better answer
        enhanced_question = f"{question}\n\nRecent web information: {search_result}"
    else:
        enhanced_question = question

    # Call OpenAI
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
                "content": "You are a helpful, smart, and friendly study assistant. Give clear, accurate answers in simple English."
            },
            {"role": "user", "content": enhanced_question}
        ],
        "temperature": 0.6,
        "max_tokens": 400
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            answer = result["choices"][0]["message"]["content"].strip()
            return answer
        else:
            return "Sorry, I couldn't generate a response. Please try again."

    except Exception as e:
        return f"Request failed: {str(e)}"


def should_search_web(question: str) -> bool:
    q = question.lower()
    triggers = ["latest", "current", "news", "today", "202", "president", "prime minister", 
                "capital", "population", "who won", "what happened", "recent"]
    return any(trigger in q for trigger in triggers)


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for g in soup.find_all('div', class_='g')[:4]:
            text = g.get_text(strip=True)
            if len(text) > 100:
                snippets.append(text[:400])
        
        return "\n\n".join(snippets) if snippets else "No clear information found."
        
    except:
        return "Could not access web information."


# For testing locally
if __name__ == "__main__":
    print(ask_ai("What is the capital of Ghana?"))
    print(ask_ai("What is a computer?"))
