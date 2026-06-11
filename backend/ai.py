import requests
from bs4 import BeautifulSoup

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Only trigger web search for specific types of questions
    search_triggers = ["latest", "current", "news", "2026", "today", "recent", "population", 
                      "who won", "what happened", "capital of", "president", "prime minister"]
    
    if any(trigger in q for trigger in search_triggers):
        search_result = web_search(question)
        if "couldn't extract" not in search_result:
            return search_result
        else:
            return f"I couldn't find the latest information right now.\n\n{general_response(question)}"
    else:
        return general_response(question)


def general_response(question: str) -> str:
    q = question.lower()
    
    if "hello" in q or "hi" in q:
        return "Hello! I'm StudyMate AI. How can I help you with your studies today?"
    elif "how are you" in q:
        return "I'm doing great! Ready to help you learn 😊"
    elif "name" in q:
        return "I'm StudyMate AI, your personal intelligent study assistant."
    else:
        return f"**Question:** {question}\n\nI'm here to help you with explanations, concepts, and study-related topics. Feel free to ask anything!"


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for g in soup.find_all('div', class_='g')[:5]:
            text = g.get_text(strip=True)
            if len(text) > 100 and "cookie" not in text.lower():
                snippets.append(text[:450])
        
        if snippets:
            return "📡 Here's what I found online:\n\n" + "\n\n".join(snippets)
        else:
            return "I searched the web but couldn't extract clear information. Can you rephrase your question?"
            
    except Exception:
        return "I'm having trouble accessing the internet right now. I'll answer based on my knowledge."


# Optional: Test function
if __name__ == "__main__":
    print(ask_ai("What is the capital of France?"))
    print(ask_ai("Explain photosynthesis"))
