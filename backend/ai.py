import requests
from bs4 import BeautifulSoup

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Force web search for any question that might need current info
    if should_search_web(q):
        search_result = web_search(question)
        if "couldn't" not in search_result and "trouble" not in search_result:
            return search_result + "\n\n(Information fetched from the web)"

    # Fallback to smart response
    return smart_response(question)


def should_search_web(question: str) -> bool:
    # Broader triggers
    triggers = ["president", "ghana", "202", "today", "current", "latest", "news", 
                "who is", "what is the", "population", "capital", "prime minister"]
    return any(t in question for t in triggers) or len(question.split()) > 4


def smart_response(question: str) -> str:
    q = question.lower()
    
    if "hello" in q or "hi" in q:
        return "Hello! 👋 How can I help you today?"
    
    elif "computer" in q:
        return """**What is a Computer?**

A computer is an electronic device that processes data according to instructions. 

It can:
- Take input (keyboard, mouse, touch)
- Process information (CPU)
- Give output (screen, speakers)
- Store data (hard drive, SSD)

Computers power smartphones, laptops, the internet, and almost all modern technology."""
    
    elif "game" in q:
        return """**What is a Game?**

A game is an activity done for enjoyment, entertainment, or learning. 

Types of games:
- Video games (Free Fire, PUBG, etc.)
- Board games (Ludo, Chess)
- Sports

Games help improve thinking skills, strategy, and reaction time."""
    
    else:
        return f"**Answer:**\n\n{question}\n\nI'm here to help you with clear explanations. Please ask more specific questions!"


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for g in soup.find_all('div', class_='g')[:5]:
            text = g.get_text(strip=True)
            if len(text) > 120:
                snippets.append(text[:600])
        
        if snippets:
            return "📡 **Fresh Information from the Web:**\n\n" + "\n\n".join(snippets)
        else:
            return "I searched the web but couldn't find clear results."
            
    except Exception:
        return "I'm having trouble accessing current information right now."


# Test function
if __name__ == "__main__":
    print(ask_ai("What is the current president of Ghana?"))
    print(ask_ai("What is a computer?"))
