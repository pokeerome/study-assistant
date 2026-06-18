# Personal Study Assistant

A local AI assistant that answers questions from your own notes via a REST API. Includes question history tracking with SQLite. No API keys or internet required.

## How it works

1. You provide a text file with your notes
2. The assistant splits it into chunks when the server starts
3. When you send a question, it searches for the most relevant chunks
4. It passes those chunks to a local AI model and returns a grounded answer
5. Every question and answer is saved to a local SQLite database

This is a simple RAG (Retrieval Augmented Generation) system built from scratch in pure Python.

## Features

- **REST API** — send questions via HTTP and get JSON responses
- **History tracking** — every question and answer saved to SQLite with timestamps
- **Fully local** — runs on your machine using Ollama, no API keys needed
- **Configurable** — chunk size, model, and file all controlled via `.env`
- **Auto docs** — FastAPI generates interactive documentation at `/docs`

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- llama3.2 model pulled (`ollama pull llama3.2`)

## Setup

1. Clone the repository
   ```
   git clone https://github.com/pokeerome/study-assistant.git
   cd study-assistant
   ```

2. Create a virtual environment
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   ```

3. Install dependencies
   ```
   pip install ollama python-dotenv fastapi uvicorn
   ```

4. Create a `.env` file in the root folder
   ```
   MODEL_NAME=llama3.2
   CHUNK_SIZE=500
   MAX_CHUNKS=3
   FILE_NAME=notes.txt
   ```

5. Add your notes to `notes.txt` (a sample file is included)

## Usage

Start the server:

```
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` in your browser to use the interactive API documentation.

---

### POST /ask

Send a question and get an answer based on your notes.

```
POST http://127.0.0.1:8000/ask
Content-Type: application/json

{
  "question": "what is RAG?"
}
```

Response:

```json
{
  "answer": "RAG stands for Retrieval Augmented Generation...",
  "relevant_chunks_found": 1
}
```

---

### GET /history

Returns all previous questions and answers with timestamps.

```
GET http://127.0.0.1:8000/history
```

Response:

```json
[
  {
    "id": 1,
    "question": "what is RAG?",
    "answer": "RAG stands for Retrieval Augmented Generation...",
    "chunks_found": 1,
    "timestamp": "2026-06-18T12:49:09.044496"
  }
]
```

---

## Project structure

```
study-assistant/
├── main.py           # FastAPI app — endpoints and request handling
├── database.py       # SQLite database logic — init, save, fetch history
├── notes.txt         # Sample notes file
├── .gitignore
└── README.md
```

## What I learned building this

- File I/O and text chunking in Python
- How to filter stop words for better search results
- How RAG works at a fundamental level — chunking, retrieval, augmented generation
- Calling a local AI model with Ollama
- Managing configuration with `.env` files
- Building a REST API with FastAPI and Pydantic
- Structuring request and response models with validation
- SQLite database integration with Python
- Separation of concerns — keeping database logic separate from API logic
- Persistent history tracking across sessions
