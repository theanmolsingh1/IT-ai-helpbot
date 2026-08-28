import os
from fastapi import FastAPI , Request
from dotenv import load_dotenv
from google import genai
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import chromadb

from backend.llm import generate_res_for_rag


# Create embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# Create ChromaDB client
client = chromadb.PersistentClient(
    path="./chroma_db"
)

# Create collection
collection = client.get_or_create_collection(
    name="troubleshooting"
)

# Text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)


def text_to_vectors(text):
    chunks = text_splitter.split_text(text)
    vectors = embeddings.embed_documents(chunks)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=vectors
    )

    return chunks


def retrieve(query):
    query_vector = embeddings.embed_query(query)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )

    return results["documents"][0]



def answer(query):
    context = "\n\n".join([query]+retrieve(query))
    return generate_res_for_rag(context)
