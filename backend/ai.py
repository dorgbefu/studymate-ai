import requests
from bs4 import BeautifulSoup

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Stronger triggers for web search
    if should_search_web(q):
        search_result = web_search(question)
        if "couldn't extract" not in search_result and "trouble accessing" not in search_result:
            return search_result
    
    # Default intelligent response
    return general_response(question)


def should_search_web(question: str) -> bool:
    triggers = [
        "president", "prime minister", "capital", "population", "who is", "what is the",
        "latest", "current", "news", "today", "202", "winner", "how many", "how much",
        "what time", "what date", "when did", "who won"
    ]
    return any(trigger in question for trigger in triggers)


def general_response(question: str) -> str:
    q = question.lower()
    
    if "hello" in q or "hi" in q:
        return "Hello! 👋 How can I help you with your studies today?"
    elif "how are you" in q:
        return "I'm doing great! Ready to assist you 😊"
    elif "name" in q:
        return "I'm StudyMate AI, your smart study assistant."
    elif "what is ai" in q or "what is artificial" in q:
        return "AI (Artificial Intelligence) is the ability of machines to perform tasks that typically require human intelligence, such as learning, reasoning, and problem-solving."
    elif "what is computer" in q:
        return "A computer is an electronic device that processes data according to instructions (programs) to perform calculations and tasks."
    else:
        return f"**Question:** {question}\n\nI'm here to help you understand concepts, solve problems, and answer study-related questions. Feel free to ask anything!"


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for g in soup.find_all('div', class_='g')[:5]:
            text = g.get_text(strip=True)
            if len(text) > 80 and "cookie" not in text.lower() and "javascript" not in text.lower():
                snippets.append(text[:550])
        
        if snippets:
            return "📡 **Latest Information from the Web:**\n\n" + "\n\n".join(snippets)
        else:
            return "I searched the web but couldn't extract clear information. Can you rephrase your question?"
            
    except Exception:
        return "I'm having trouble accessing the internet right now."


# Test
if __name__ == "__main__":
    print(ask_ai("What is the president of Ghana?"))
    print(ask_ai("What is AI?"))
    print(ask_ai("What is today's date?"))
