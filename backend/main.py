from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from ai import ask_ai  # Keep your existing AI logic

app = FastAPI(title="StudyMate AI")

class Question(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>StudyMate AI</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            #chat { width: 700px; height: 400px; border: 1px solid #ccc; overflow-y: auto; padding: 10px; background: #f9f9f9; }
            input { width: 500px; padding: 10px; font-size: 16px; }
            button { padding: 10px 20px; font-size: 16px; }
        </style>
    </head>
    <body>
        <h1>StudyMate AI</h1>
        <div id="chat"></div>
        <br>
        <input type="text" id="question" placeholder="Ask anything..." size="60">
        <button onclick="askAI()">Send</button>

        <script>
        async function askAI() {
            const input = document.getElementById("question");
            const chat = document.getElementById("chat");
            const question = input.value.trim();
            
            if (!question) return;

            chat.innerHTML += `<b>You:</b> ${question}<br>`;
            chat.innerHTML += `AI: Thinking...<br>`;
            chat.scrollTop = chat.scrollHeight;

            try {
                const response = await fetch("/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: question })
                });
                const data = await response.json();
                chat.innerHTML = chat.innerHTML.replace("Thinking...", data.answer);
            } catch (e) {
                chat.innerHTML = chat.innerHTML.replace("Thinking...", "❌ Connection error");
            }

            input.value = "";
            chat.scrollTop = chat.scrollHeight;
        }
        </script>
    </body>
    </html>
    """

@app.post("/ask")
def ask(question: Question):
    answer = ask_ai(question.question)
    return {"answer": answer}
