from fastapi import FastAPI , Request, Form
from fastapi.templating import Jinja2Templates
from pathlib import Path
from bson import ObjectId

from backend.llm import generate_intent
from backend.llm import generate_ticket_id, generate_general_response
from backend.troubleshoot import read_pdfs
from backend.rag import answer, text_to_vectors
from backend.config import db
from backend.model import Ticket

ticket_collection = db["tickets"]

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
        return template.TemplateResponse(
            request=request,
            name="solution.html",
            context={
                "query":query,
                "result":solution
            }
        )

    elif intent == "create_ticket":
            ticket = Ticket(
                description=query,
                status="Pending"
            )
            result = ticket_collection.insert_one(
                ticket.model_dump()
            )
            return template.TemplateResponse(
                request=request,
                name="ticket_created.html",
                context={
                    "query":query,
                    "ticket_id":str(result.inserted_id)
                }
            )

    elif intent == "ticket_status":
        ticket_id = generate_ticket_id(query)
        ticket = ticket_collection.find_one(
            {"_id":ObjectId(ticket_id)}
        )
        return template.TemplateResponse(
            request=request,
            name="status.html",
            context={
                "query":query,
                "status":ticket["status"],
                "date":ticket["date"]
            }
        )

    # else: #for general query
    else:
        general_response = generate_general_response(query)
        return template.TemplateResponse(
            request=request,
            name="general_response.html",
            context={
                general_response
            }
        )
                      
