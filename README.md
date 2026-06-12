# Personal Study Assistant

A CLI-based AI assistant that answers questions from your own notes using local AI — no API keys or internet required.

## How it works

1. You provide a text file with your notes
2. The assistant splits it into chunks
3. When you ask a question, it finds the most relevant chunks
4. It passes those chunks to a local AI model and returns an answer

This is a simple RAG (Retrieval Augmented Generation) system built from scratch in pure Python.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- llama3.2 model pulled (`ollama pull llama3.2`)

## Setup

1. Clone the repository
   git clone https://github.com/pokeerome/study-assistant.git
   cd study-assistant

2. Create a virtual environment
   python -m venv venv
   venv\Scripts\activate  (Windows)
   source venv/bin/activate  (Mac/Linux)

3. Install dependencies
   pip install ollama python-dotenv

4. Create a .env file (see below)

5. Add your notes to a .txt file

6. Run the assistant
   python assistant.py

## .env file

Create a .env file in the root folder with these values:

   MODEL_NAME=llama3.2
   CHUNK_SIZE=500
   MAX_CHUNKS=3
   FILE_NAME=notes.txt

## Example usage

   Loading file: notes.txt
   Done! File has 850 characters.
   Split into 4 chunks.

   Ready! Type your question or 'quit' to exit.

   You: what is RAG?
   Found 1 relevant chunks.
   Assistant: RAG stands for Retrieval Augmented Generation...

   You: quit
   Goodbye!

## What I learned building this

- File I/O and text chunking in Python
- How to filter stop words for better search results
- How RAG works at a fundamental level
- Calling a local AI model with Ollama
- Managing configuration with .env files