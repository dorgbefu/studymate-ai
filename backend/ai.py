import requests
from bs4 import BeautifulSoup
from datetime import datetime

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    print(f"DEBUG: Received question: {question}")  # For Render logs
    
    # Direct answers
    if "today" in q and ("date" in q or "day" in q):
        return f"**Today's Date:**\n{datetime.now().strftime('%A, %B %d, %Y')}"
    
    if "president of ghana" in q or "ghana president" in q:
        return "**President of Ghana:**\nJohn Dramani Mahama (since January 7, 2025)"
    
    if "japan" in q and ("prime minister" in q or "president" in q):
        return "**Prime Minister of Japan:**\nSanae Takaichi (since October 21, 2025)"
    
    # Force web search for everything else
    print(f"DEBUG: Calling web_search for: {question}")
    result = web_search(question)
    print(f"DEBUG: Web search returned: {result[:100]}...")  # Truncated
    return result


def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"DEBUG: Google status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        snippets = []
        for element in soup.find_all(['div', 'span', 'p', 'h1', 'h2']):
            text = element.get_text(strip=True)
            if 80 < len(text) < 650 and "cookie" not in text.lower():
                snippets.append(text)
                if len(snippets) >= 5:
                    break
        
        if snippets:
            return "**📡 Web Search Result:**\n\n" + "\n\n".join(snippets[:3])
        return "I searched but found no clear information."
        
    except Exception as e:
        return f"Web search error: {str(e)[:100]}"


if __name__ == "__main__":
    print(ask_ai("what is matter"))
