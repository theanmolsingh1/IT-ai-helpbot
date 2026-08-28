import os
from fastapi import FastAPI , Request
from google import genai
from dotenv import load_dotenv

from pathlib import Path
import fitz  # PyMuPDF


# from backend.rag import answer, text_to_vectors

load_dotenv()
# pdf reading.
DOCS_DIR = Path(__file__).parent.parent / "doc"
def read_pdfs():
    text = ""

    for pdf_file in sorted(DOCS_DIR.glob("*.pdf")):
        text += f"\n\n===== {pdf_file.name} =====\n\n"

        pdf = fitz.open(pdf_file)

        for page in pdf:
            text += page.get_text()

        pdf.close()

    return text
