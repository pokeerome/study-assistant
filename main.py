import os
import ollama
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
MAX_CHUNKS = int(os.getenv("MAX_CHUNKS", 3))
FILE_NAME = os.getenv("FILE_NAME", "notes.txt")

print(f"Loading file: {FILE_NAME}")

chunks = []

try:
    with open(FILE_NAME, 'r', encoding="utf-8") as f:
        text = f.read()
        characters = len(text)

        for i in range(0, characters, CHUNK_SIZE):
            chunks.append(text[i:i + CHUNK_SIZE])

        with open('chunks.txt', 'w', encoding='utf-8') as f:
            f.write("\n\n==========\n\n".join(chunks))
        
        print(f"Done! File has {characters} characters")
        print(f"Split into {len(chunks)} chunks")

except FileNotFoundError:
    print("File not found!")
    exit()

print("Ready! Type your question or 'quit' to exit.")

while True:
    user_ans = input("Type your question: ")

    if user_ans.lower() == "quit":
        print("Goodbye!")
        break

    stop_words = {"what", "is", "a", "the", "how", "does", "can", "are", "in", "of", "to"}

    question_words = []

    for w in user_ans.lower().split():
        if w not in stop_words:
            question_words.append(w)

    found_chunks = []

    for chunk in chunks:
        chunk_lower = chunk.lower()

        for word in question_words:
            if word in chunk_lower:
                found_chunks.append(chunk)
                break  

    found_chunks = found_chunks[:MAX_CHUNKS]

    with open('found_chunks.txt', 'w') as f:
        f.write("\n\n".join(found_chunks))

    if not found_chunks:
        print("No relevant chunks found for that question.")
    else:
        print(f"Found {len(found_chunks)} relevant chunks.")
        context = "\n\n".join(found_chunks)
        system_prompt = f"You are a helpful assistant. Answer questions using only the context below. If the answer is not in the context, say you don't know.\n\nContext:\n{context}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_ans},
        ]

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages,
        )

        print(response.message.content)