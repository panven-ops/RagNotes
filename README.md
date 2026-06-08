
# RAG Notes

A local RAG (Retrieval-Augmented Generation) system for querying your own PDF notes using natural language. Designed to run on low-resource hardware and respond in Greek.

## Features
- Ingests PDF files and splits them into searchable chunks
- Answers questions based strictly on your notes
- Responds in Greek
- If the answer is not found in the notes, it says so
- Optimized for low RAM usage via sequential model loading

## Tech Stack
**PDF Processing:** PyMuPDF (fitz)

**Embeddings:** FastEmbed (paraphrase-multilingual-MiniLM-L12-v2)

**Vector Database:** ChromaDB

**LLM:** Ollama (llama3.2:1b)

## Project Structure

- ingest.py 
- query.py
- pdfs
- chroma_db

## How It Works

### Phase 1 — Ingest
    1. Reads all PDFs from the `pdfs/` folder
    2. Splits text into overlapping chunks (400 words, 50 word overlap)
    3. Generates embeddings with FastEmbed
    4. Stores chunks + embeddings in ChromaDB

### Phase 2 — Query
    1. Embeds the user's question
    2. Retrieves the top 3 most relevant chunks from ChromaDB
    3. Frees the embedding model from RAM (gc.collect())
    4. Passes chunks as context to Ollama
    5. Returns the answer in Greek
    6. Reloads the embedding model for the next question

> The sequential loading/unloading of models between steps is intentional — it keeps RAM usage low enough to run on constrained hardware.

## Getting Started

### Prerequisites
- Python 3.12
- [Ollama](https://ollama.com) installed and running

Pull the model before first use:
```bash
ollama pull llama3.2:1b
```

### Installation
```bash
git clone https://github.com/panven-ops/RagNotes
cd RagNotes
pip install -r requirements.txt
```

Add your PDF files to the `pdfs/` folder.

### Usage
First, ingest your PDFs:
```bash
python3 ingest.py
```

Then start querying:
```bash
python3 query.py
```

Type `exit` to quit.

## Configuration

These constants can be adjusted at the top of each file:

| Variable | Default | Description |
|---|---|---|
| `TEXT_CHUNK_SIZE` | 400 | Words per chunk |
| `CHUNK_OVERLAP` | 50 | Overlapping words between chunks |
| `TOP_K` | 3 | Number of chunks retrieved per query |
| `OLLAMA_MODEL` | llama3.2:1b | Ollama model to use |

## License
[MIT](https://choosealicense.com/licenses/mit/)
