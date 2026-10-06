from fastapi import FastAPI
from pydantic import BaseModel
import os
from rag import load_repository, ask_question
app = FastAPI(
    title="GitHub Repository Q&A API"
)
class Repository(BaseModel):

    github_url: str
class Question(BaseModel):

    question: str

@app.get("/")
def home():    

    return {
        "message": "GitHub RAG API is running"
    }

@app.post("/load")
def load_repo(data: Repository):

    result = load_repository(
        data.github_url
    )

    return {
        "message": result
    }

@app.post("/ask")

def ask(data: Question):

    answer = ask_question(
        data.question
    )

    return {
        "question": data.question,
        "answer": answer
    }