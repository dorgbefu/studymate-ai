import requests
from bs4 import BeautifulSoup
from datetime import datetime

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Direct factual answers
    if "today" in q and ("date" in q or "day" in q):
        today = datetime.now().strftime("%A, %B %d, %Y")
        return f"**Today's Date:**\n{today}"
    
    if "time" in q:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"**Current Time:** {current_time}"
    
    # Try web search for current events / people
    if should_search_web(q):
        result = web_search(question)
        if "trouble" not in result.lower() and "couldn't" not in result.lower():
            return result
    
    return educational_response(question)


def should_search_web(question: str) -> bool:
    triggers = ["president", "prime minister", "pm", "who is", "current", "latest", 
                "ghana", "japan", "today", "date", "202"]
    return any(t in question.lower() for t in triggers)


def educational_response(question: str) -> str:
    q = question.lower()
    if "hello" in q or "hi" in q:
        return "Hello! 👋 How can I help you with your studies today?"
    
    elif "computer" in q:
        return """**What is a Computer?** ..."""  # keep your original text
    
    elif "game" in q:
        return """**What is a Game?** ..."""  # keep your original
    
    elif "ai" in q:
        return """**What is Artificial Intelligence?** ..."""  # keep your original
    
    else:
        return f"I'm still learning more topics.\n\nTry asking:\n• What is today's date?\n• Who is the president of Ghana?\n• What is a computer?"


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # More robust snippet extraction
        snippets = []
        for tag in soup.find_all(['div', 'span', 'p'], string=True):
            text = tag.get_text(strip=True)
            if 80 < len(text) < 700 and not any(x in text.lower() for x in ["cookie", "consent", "javascript"]):
                snippets.append(text)
                if len(snippets) >= 4:
                    break
        
        if snippets:
            return "📡 **Fresh Information:**\n\n" + "\n\n".join(snippets[:3])
        return "I found information but couldn't extract it clearly."
        
    except Exception:
        return "I'm having trouble accessing the web right now."


# Test
if __name__ == "__main__":
    print(ask_ai("who is the president of ghana"))
    print(ask_ai("who is the prime minister of japan"))
    print(ask_ai("what is today's date"))
