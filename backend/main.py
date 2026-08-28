from fastapi import FastAPI , Request, Form
from fastapi.templating import Jinja2Templates
from pathlib import Path

from backend.llm import generate_intent
from backend.troubleshoot import read_pdfs
from backend.rag import answer, text_to_vectors

app = FastAPI()

template = Jinja2Templates(directory="templates")

text = read_pdfs()
text_to_vectors(text)

@app.get("/")
def home(request : Request):
    return template.TemplateResponse(
        request = request,
        name = "index.html"
    )

@app.get("/chat")
def goto_chat(request: Request):
    return template.TemplateResponse(
        request = request,
        name = "chat.html"
    )

@app.post("/search")
def search(request : Request , query : str  = Form(...)):
    intent = generate_intent(query)

    if intent == "troubleshooting":
        solution = answer(query)

    # elif intent == "create_ticket":

    # elif intent == "ticket_status":

    # else: #for general query

    