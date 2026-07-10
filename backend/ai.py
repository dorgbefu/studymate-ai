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
    
    # Try web search for dynamic questions
    if should_search_web(q):
        result = web_search(question)
        if "trouble" not in result.lower() and "couldn't" not in result.lower():
            return result
    
    # Educational responses for study topics
    return educational_response(question)


def should_search_web(question: str) -> bool:
    triggers = [
        "president", "prime minister", "who is", "current", "latest", "news",
        "today", "202", "population", "capital", "ghana", "japan", "matter"
    ]
    return any(trigger in question for trigger in triggers)


def educational_response(question: str) -> str:
    q = question.lower()
    
    if "computer" in q:
        return """**What is a Computer?**
A computer is an electronic device that processes data according to a set of instructions (a program).

**Main Functions:**
- Input (keyboard, mouse, touchscreen)
- Processing (CPU)
- Output (screen, speakers, printer)
- Storage (RAM, SSD, Hard Drive)

Computers power smartphones, laptops, and the internet."""
    
    elif "matter" in q:
        return """**What is Matter?**
Matter is anything that has mass and takes up space. It is the "stuff" that makes up the universe.

**States of Matter:**
- Solid (ice, rock)
- Liquid (water)
- Gas (air, oxygen)
- Plasma (stars, lightning)

Everything you can touch is made of matter."""
    
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
        for g in soup.find_all('div', class_=True)[:8]:
            text = g.get_text(strip=True)
            if 120 < len(text) < 650 and "cookie" not in text.lower():
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
    print(ask_ai("what is today's date"))
