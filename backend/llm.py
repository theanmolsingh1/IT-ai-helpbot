from fastapi import FastAPI, Request
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


# intention generation section.
def generate_intent(query):
   prompt = f"""
You are an IT helpdesk intent classifier.

Classify the user's query into exactly ONE of these intents:

1. troubleshooting
   - Problems with laptop, VPN, WiFi, email, software, printer, etc.

2. create_ticket
   - User wants to create, raise, or submit an IT support ticket.

3. ticket_status
   - User wants to check the status of an existing ticket.

4. general_query
   - General IT questions that don't fit the other categories.

Return ONLY the intent name.
Do not explain your answer.

User query:
{query}
"""
   response  = client.models.generate_content(
        model="gemini-3.6-flash",
        contents = prompt   
    )
   return response.text.strip().lower()



# for troubleshhoting response.
def generate_res_for_rag(query):
   prompt = f"""
   - you are a bot who will get query and their context from rag system.
   - your task is to make a clear and presentable output for this.
   - dont send any unnecessary response.
   - no hey hi hello or anything.

   user context:
   {query}
"""
   response  = client.models.generate_content(
        model="gemini-3.6-flash",
        contents = prompt   
   )
   return response