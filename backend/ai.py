import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def ask_ai(question: str) -> str:
    q = question.lower().strip()
    
    # Use Tavily for questions that need current info
    if should_use_search(q):
        return tavily_search(question)
    else:
        return general_knowledge(question)


def should_use_search(question: str) -> bool:
    keywords = ["latest", "current", "news", "today", "2026", "who is", "what is the", 
                "president", "prime minister", "population", "capital", "winner", 
                "happened", "recent", "how many"]
    return any(k in question for k in keywords)


def tavily_search(query: str) -> str:
    if not TAVILY_API_KEY:
        return "Tavily API key is not configured."

    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": "basic",
            "max_results": 5
        }
        
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()

        if "results" in data and data["results"]:
            results = []
            for item in data["results"][:3]:
                results.append(f"• {item['title']}\n{item['content'][:300]}...")
            return "📡 **Latest Information:**\n\n" + "\n\n".join(results)
        else:
            return "I couldn't find relevant information. Can you rephrase?"

    except Exception as e:
        return f"Search error: {str(e)}"


def general_knowledge(question: str) -> str:
    q = question.lower()
    if "hello" in q or "hi" in q:
        return "Hello! 👋 How can I help you today?"
    elif "what is ai" in q or "artificial intelligence" in q:
        return "AI (Artificial Intelligence) is the simulation of human intelligence in machines..."
    else:
        return f"**Answer:**\n\nI'm here to help you with explanations and study topics. Ask me anything!"


# Test
if __name__ == "__main__":
    print(ask_ai("Who is the current president of Ghana?"))
    print(ask_ai("What is today's date?"))
