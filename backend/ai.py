import requests
from bs4 import BeautifulSoup
from datetime import datetime

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Direct fast answers
    if "today" in q and ("date" in q or "day" in q):
        return f"**Today's Date:**\n{datetime.now().strftime('%A, %B %d, %Y')}"
    
    if "time" in q:
        return f"**Current Time:** {datetime.now().strftime('%I:%M %p')}"
    
    # Direct known answers
    if "president of ghana" in q or "ghana president" in q:
        return "**President of Ghana:**\nJohn Dramani Mahama (since January 7, 2025)"
    
    if "prime minister of japan" in q or "japan prime minister" in q or "president of japan" in q:
        return "**Prime Minister of Japan:**\nSanae Takaichi (since October 21, 2025)"
    
    # Try web search for EVERYTHING else
    result = web_search(question)
    if "trouble" not in result.lower():
        return result
    
    # Ultimate fallback (very rare now)
    return f"**Answer for:** {question}\n\nI searched the web but couldn't find a clear answer. Try rephrasing your question more specifically."


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=12)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        # Extract more possible text blocks
        for element in soup.find_all(['div', 'span', 'p', 'h1', 'h2', 'h3', 'li']):
            text = element.get_text(strip=True)
            if 80 < len(text) < 700 and not any(x in text.lower() for x in ["cookie", "consent", "javascript", "sign in", "privacy"]):
                snippets.append(text)
                if len(snippets) >= 5:
                    break
        
        if snippets:
            return "**📡 Web Search Result:**\n\n" + "\n\n".join(snippets[:4])
        
        return f"I searched for '**{query}**' but couldn't extract clear information."
        
    except Exception as e:
        return "I'm having trouble connecting to the web right now. Please try again."


# Test
if __name__ == "__main__":
    print(ask_ai("what is a computer"))
    print(ask_ai("who is the president of ghana"))
    print(ask_ai("what is orange"))
    print(ask_ai("what is matter"))
    print(ask_ai("what is today's date"))
