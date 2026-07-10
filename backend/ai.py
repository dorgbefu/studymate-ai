import requests
from bs4 import BeautifulSoup
from datetime import datetime

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Special fast answers
    if "today" in q and ("date" in q or "day" in q):
        return f"**Today's Date:**\n{datetime.now().strftime('%A, %B %d, %Y')}"
    
    if "time" in q:
        return f"**Current Time:** {datetime.now().strftime('%I:%M %p')}"
    
    # Always try web search first
    result = web_search(question)
    if "trouble" not in result.lower() and "couldn't" not in result.lower():
        return result
    
    # Only use this if web search completely fails
    return f"I searched the web but couldn't get a clear answer for:\n**{question}**\n\nTry rephrasing your question."


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        # Try multiple possible containers
        for element in soup.find_all(['div', 'span', 'p', 'h1', 'h2', 'h3']):
            text = element.get_text(strip=True)
            if 100 < len(text) < 700 and not any(word in text.lower() for word in ["cookie", "consent", "javascript", "sign in"]):
                snippets.append(text)
                if len(snippets) >= 5:
                    break
        
        if snippets:
            clean_snippets = "\n\n".join(snippets[:4])
            return f"**Answer from the Web:**\n\n{clean_snippets}"
        
        return "I searched the web but couldn't extract clear information."
        
    except Exception as e:
        return f"I'm having trouble accessing the web right now. ({str(e)[:100]})"


# For testing
if __name__ == "__main__":
    print(ask_ai("who is the president of ghana"))
    print(ask_ai("what is today's date"))
    print(ask_ai("what is the capital of japan"))
    print(ask_ai("tell me about artificial intelligence"))
