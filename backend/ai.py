import requests
from bs4 import BeautifulSoup

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # More intelligent trigger for web search
    if should_search_web(q):
        search_result = web_search(question)
        if "couldn't extract" not in search_result and "trouble accessing" not in search_result:
            return search_result
        else:
            return f"{general_response(question)}\n\n(Note: I couldn't fetch latest web info right now.)"
    else:
        return general_response(question)


def should_search_web(question: str) -> bool:
    """Decide when to search the web"""
    triggers = [
        "latest", "current", "news", "today", "202", "who is", "what is the capital",
        "population", "president", "prime minister", "winner", "happened", "recent",
        "how many", "how much", "what time", "what date"
    ]
    return any(trigger in question for trigger in triggers)


def general_response(question: str) -> str:
    q = question.lower()
    
    if "hello" in q or "hi " in q or q == "hi":
        return "Hello! 👋 How can I help you with your studies today?"
    elif "how are you" in q:
        return "I'm doing great! Ready to assist you with learning 😊"
    elif "name" in q:
        return "I'm StudyMate AI, your personal study assistant powered by AI."
    elif "what is computer" in q or "computer" in q:
        return "A computer is an electronic device that can be programmed to carry out sequences of arithmetic or logical operations automatically."
    elif "date" in q or "today" in q:
        return "I don't have real-time clock access in this mode. You can ask me 'What is today's date?' and I'll try to search the web."
    else:
        return f"**Question:** {question}\n\nI'm here to help you with explanations, concepts, and study-related topics. Feel free to ask anything!"


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for g in soup.find_all('div', class_='g')[:4]:
            text = g.get_text(strip=True)
            if len(text) > 100 and "cookie" not in text.lower():
                snippets.append(text[:500])
        
        if snippets:
            return "📡 **Here's what I found on the web:**\n\n" + "\n\n".join(snippets)
        else:
            return "I searched the web but couldn't extract clear information. Can you rephrase your question?"
            
    except Exception:
        return "I'm having trouble accessing the internet right now."


# For testing
if __name__ == "__main__":
    print(ask_ai("What is today's date?"))
    print(ask_ai("What is a computer?"))
    print(ask_ai("Explain photosynthesis"))
