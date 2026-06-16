import os
import ollama
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
MAX_CHUNKS = int(os.getenv("MAX_CHUNKS", 3))
FILE_NAME = os.getenv("FILE_NAME", "notes.txt")

app = FastAPI()

class Question(BaseModel):
    question: str = Field(min_length=3, max_length=500)

class Answer(BaseModel):
    answer: str
    relevant_chunks_found: int

chunks = []

try:
    with open(FILE_NAME, 'r', encoding="utf-8") as f:
        text = f.read()
        characters = len(text)

        for i in range(0, characters, CHUNK_SIZE):
            chunks.append(text[i:i + CHUNK_SIZE])

        print(f"Done! File has {characters} characters")
        print(f"Split into {len(chunks)} chunks")
        print("Server ready! POST to http://127.0.0.1:8000/ask")

except FileNotFoundError:
    print(f"File not found: {FILE_NAME}")
    exit()

@app.post("/ask", response_model=Answer)
def ask_question(user_question: Question):
    stop_words = {"what", "is", "a", "the", "how", "does", "can", "are", "in", "of", "to"}

    question_words = [
        w for w in user_question.question.lower().split()
        if w not in stop_words
    ]

    found_chunks = []

    for chunk in chunks:
        chunk_lower = chunk.lower()
        for word in question_words:
            if word in chunk_lower:
                found_chunks.append(chunk)
                break

    found_chunks = found_chunks[:MAX_CHUNKS]

    if not found_chunks:
        return Answer(answer = "No relevant information found for that question.", relevant_chunks_found = 0)

    context = "\n\n".join(found_chunks)
    system_prompt = f"You are a helpful assistant. Answer questions using only the context below. If the answer is not in the context, say you don't know.\n\nContext:\n{context}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question.question},
    ]

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
    )

    return Answer(answer = response.message.content, relevant_chunks_found = len(found_chunks))