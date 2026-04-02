from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from ai import ask_ai

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>StudyMate AI</title>
    </head>
    <body>
        <h1>StudyMate AI</h1>

        <div id="chat" style="width:600px;height:300px;border:1px solid black;overflow:auto;padding:10px;"></div>
        <br>

        <input type="text" id="question" placeholder="Ask a question" size="50">
        <button onclick="askAI()">Ask</button>

        <script>
        async function askAI() {
            const questionBox = document.getElementById("question");
            const chat = document.getElementById("chat");
            const question = questionBox.value;

            chat.innerHTML += "<b>You:</b> " + question + "<br>";
            chat.innerHTML += "AI: Thinking...<br>";

            const response = await fetch("/ask", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    question: question
                })
            });

            const data = await response.json();

            chat.innerHTML = chat.innerHTML.replace("Thinking...", data.answer);
            questionBox.value = "";
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
