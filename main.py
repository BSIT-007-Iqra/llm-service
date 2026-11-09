import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

BACKEND = os.getenv("BACKEND", "mock")  # "mock" or "ollama"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3.2:1b")

app = FastAPI(title="LLM Service")


class Question(BaseModel):
    question: str


def generate(prompt: str) -> str:
    if BACKEND == "mock":
        return f"[mock answer] You asked: {prompt}"
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=300,
    )
    r.raise_for_status()
    return r.json()["response"]


@app.get("/health")
def health():
    return {"status": "ok", "backend": BACKEND}


@app.post("/ask")
def ask(body: Question):
    try:
        return {"answer": generate(body.question)}
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Backend error: {e}")
