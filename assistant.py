import os
import ollama
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel, Field
from database import init_db, save_history, get_history as fetch_history

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

class History(BaseModel):
    id: int
    question: str
    answer: str
    chunks_found: int
    timestamp: str

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

init_db()

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
    system_prompt = f"""You are a helpful assistant that answers ONLY using the exact information in the context below.
    Do NOT add any information that is not explicitly written in the context.
    Do NOT expand on topics using outside knowledge.
    If the context only has limited information, give only that limited information and nothing more.
    If the answer cannot be found at all in the context, respond with: "I don't know based on the provided notes."
    If you are unsure whether information comes from the context or your training, do NOT include it.
    \n\nContext:\n{context}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question.question},
    ]

    response = ollama.chat(
        model=MODEL_NAME,
        messages=messages,
    )

    save_history(user_question.question, response.message.content, len(found_chunks))

    return Answer(answer = response.message.content, relevant_chunks_found = len(found_chunks))

@app.get("/history", response_model=list[History])
def get_history():
    rows = fetch_history()
    history_list = []
    for row in rows:
        history_list.append(History(id=row[0], question=row[1], answer=row[2], chunks_found=row[3], timestamp=row[4]))
    return history_list