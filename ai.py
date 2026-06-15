import requests
from bs4 import BeautifulSoup

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Try web search for questions that likely need current info
    if should_search_web(q):
        search_result = web_search(question)
        if "couldn't" not in search_result and "trouble" not in search_result:
            return search_result
    
    # Give good educational response
    return educational_response(question)


def should_search_web(question: str) -> bool:
    triggers = [
        "president", "ghana", "capital", "population", "prime minister",
        "latest", "current", "news", "today", "202", "who is", "what is the"
    ]
    return any(trigger in question for trigger in triggers)


def educational_response(question: str) -> str:
    q = question.lower()
    
    if "hello" in q or "hi" in q:
        return "Hello! 👋 How can I help you with your studies today?"
    
    elif "computer" in q:
        return """**What is a Computer?**

A computer is an electronic device that processes data according to a set of instructions (a program).

**Main Functions:**
- Takes input (keyboard, mouse, touchscreen)
- Processes data (CPU)
- Gives output (screen, speakers, printer)
- Stores data (RAM, SSD, Hard Drive)

Computers power smartphones, laptops, the internet, and almost all modern technology."""

    elif "game" in q:
        return """**What is a Game?**

A game is a structured activity done for enjoyment, entertainment, or learning.

**Types of Games:**
- Video Games (Free Fire, PUBG, Minecraft)
- Board Games (Chess, Ludo)
- Sports Games

Games help develop strategy, quick thinking, and problem-solving skills."""

    elif "ai" in q or "artificial intelligence" in q:
        return """**What is Artificial Intelligence (AI)?**

AI is the ability of machines to perform tasks that normally require human intelligence, such as understanding language, recognizing images, and learning from experience.

Popular examples: ChatGPT, Grok, Gemini."""

    else:
        return f"**Question:** {question}\n\nI'm here to help you understand concepts clearly. Feel free to ask more specific questions!"


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for g in soup.find_all('div', class_='g')[:5]:
            text = g.get_text(strip=True)
            if len(text) > 120 and "cookie" not in text.lower():
                snippets.append(text[:550])
        
        if snippets:
            return "📡 **Fresh Information from the Web:**\n\n" + "\n\n".join(snippets)
        else:
            return "I searched the web but couldn't extract clear information."
            
    except Exception:
        return "I'm having trouble accessing current information right now."


# Test
if __name__ == "__main__":
    print(ask_ai("What is a computer?"))
    print(ask_ai("What is the name of Ghana President?"))
    print(ask_ai("What is today's date?"))
