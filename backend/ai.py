import requests
from bs4 import BeautifulSoup
from datetime import datetime

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Direct handling for common questions
    if "today" in q and ("date" in q or "day" in q):
        today = datetime.now().strftime("%A, %B %d, %Y")
        return f"**Today's Date:**\n{today}"
    
    elif "time" in q:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"**Current Time:** {current_time}"
    
    # Try web search for factual/current questions
    if should_search_web(q):
        search_result = web_search(question)
        if "couldn't" not in search_result.lower() and "trouble" not in search_result.lower():
            return search_result
    
    # Educational response
    return educational_response(question)


def should_search_web(question: str) -> bool:
    triggers = [
        "president", "ghana", "capital", "population", "prime minister",
        "latest", "current", "news", "today", "202", "who is", "what is the",
        "date", "time", "weather", "score"
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
- Sports

Games help develop strategy, quick thinking, and problem-solving skills."""
    
    elif "ai" in q or "artificial intelligence" in q:
        return """**What is Artificial Intelligence (AI)?**
AI is the ability of machines to perform tasks that normally require human intelligence, such as understanding language, recognizing images, and learning from experience.

Popular examples: ChatGPT, Grok, Gemini."""
    
    else:
        # Better fallback
        return f"**Question:** {question}\n\nI don't have a specific answer for this yet. Could you ask it more specifically? For example:\n- What is a computer?\n- Who is the president of Ghana?"


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to get better snippets
        snippets = []
        for g in soup.find_all(['div', 'span'], class_=lambda x: x and ('g' in x or 'VwiC3b' in x or 'hgKElc' in x))[:6]:
            text = g.get_text(strip=True)
            if len(text) > 80 and "cookie" not in text.lower() and "consent" not in text.lower():
                snippets.append(text[:600])
        
        if snippets:
            return "📡 **Information from the web:**\n\n" + "\n\n".join(snippets[:3])
        else:
            return "I searched the web but couldn't extract clear information."
            
    except Exception as e:
        return "I'm having trouble accessing current information right now."


# Test
if __name__ == "__main__":
    print(ask_ai("What is a computer?"))
    print(ask_ai("What is the name of Ghana President?"))
    print(ask_ai("What is today's date?"))
    print(ask_ai("Who is the president of Ghana?"))
