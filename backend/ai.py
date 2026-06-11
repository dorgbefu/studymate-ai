import requests
from bs4 import BeautifulSoup

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Trigger web search for factual/current questions
    if any(keyword in q for keyword in ["what", "who", "when", "where", "current", "latest", "news", "2026", "today", "population", "capital"]):
        return web_search(question)
    
    # Use your existing logic or simple responses
    if "hello" in q or "hi" in q:
        return "Hello! How can I help you with your studies today?"
    elif "how are you" in q:
        return "I'm doing great! Ready to assist you."
    elif "name" in q:
        return "I'm StudyMate AI, your intelligent study companion."
    else:
        return f"Based on your question: '{question}'\n\nI'm here to help with studies, explanations, and current information."


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = requests.get(url, headers=headers, timeout=8)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for result in soup.find_all('div', class_='g')[:4]:
            text = result.get_text()
            if len(text) > 60:
                snippets.append(text.strip()[:400])
        
        if snippets:
            return "📚 Here's what I found on the internet:\n\n" + "\n\n".join(snippets)
        else:
            return "I searched the web but couldn't extract clear information. Can you rephrase your question?"
            
    except Exception:
        return "I'm having trouble accessing the internet right now. I'll answer based on my knowledge."
