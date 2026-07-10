import requests
from bs4 import BeautifulSoup
from datetime import datetime

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Fast direct answers
    if "today" in q and ("date" in q or "day" in q):
        return f"**Today's Date:**\n{datetime.now().strftime('%A, %B %d, %Y')}"
    
    if "time" in q:
        return f"**Current Time:** {datetime.now().strftime('%I:%M %p')}"
    
    # Direct answers for leaders (most reliable)
    if "president of ghana" in q or "ghana president" in q:
        return "**President of Ghana:**\nJohn Dramani Mahama (since January 7, 2025)"
    
    if "prime minister of japan" in q or "japan prime minister" in q or "president of japan" in q:
        return "**Prime Minister of Japan:**\nSanae Takaichi (since October 21, 2025)"
    
    # Try web search for dynamic questions
    if should_search_web(q):
        result = web_search(question)
        if "trouble" not in result.lower() and "couldn't" not in result.lower():
            return result
    
    # Educational responses for study topics
    return educational_response(question)


def should_search_web(question: str) -> bool:
    q = question.lower()
    triggers = [
        "president", "prime minister", "who is", "current", "latest", 
        "news", "today", "202", "population", "capital", "ghana", "japan", "matter"
    ]
    return any(trigger in q for trigger in triggers)


def educational_response(question: str) -> str:
    q = question.lower()
    
    if "computer" in q:
        return """**What is a Computer?**
A computer is an electronic device that processes data according to a set of instructions (a program).

**Main Functions:**
- Takes input (keyboard, mouse, touchscreen)
- Processes data (CPU)
- Gives output (screen, speakers, printer)
- Stores data (RAM, SSD, Hard Drive)

Computers power smartphones, laptops, the internet, and almost all modern technology."""
    
    elif "matter" in q:
        return """**What is Matter?**
Matter is anything that has mass and takes up space. It is the "stuff" that makes up the universe.

**States of Matter:**
- Solid (ice, rock)
- Liquid (water, oil)
- Gas (air, oxygen)
- Plasma (in stars and lightning)

Matter can change states but cannot be created or destroyed easily."""
    
    elif "hello" in q or "hi" in q:
        return "Hello! 👋 How can I help you with your studies today?"
    
    else:
        return f"I don't have a strong answer for '**{question}**' yet.\n\nTry asking about:\n• What is a computer?\n• What is matter?\n• Who is the president of Ghana?\n• What is today's date?"


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for g in soup.find_all('div', class_=True)[:10]:
            text = g.get_text(strip=True)
            if 100 < len(text) < 650 and "cookie" not in text.lower() and "consent" not in text.lower():
                snippets.append(text[:600])
                if len(snippets) >= 4:
                    break
        
        if snippets:
            return "**📡 Information from the Web:**\n\n" + "\n\n".join(snippets[:3])
        return "I searched but couldn't extract clear information."
        
    except Exception:
        return "I'm having trouble accessing the web right now."


# Test
if __name__ == "__main__":
    print(ask_ai("what is a computer"))
    print(ask_ai("what is matter"))
    print(ask_ai("who is the president of ghana"))
    print(ask_ai("who is the prime minister of japan"))
    print(ask_ai("what is today's date"))
