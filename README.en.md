# Docsage

PDF Q&A agent using LangChain.

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com)

## Architecture

```mermaid
graph TB
    subgraph Frontend
        UI[Next.js UI]
        Upload[PDF Upload]
        Chat[Chat Interface]
    end
    
    subgraph Backend
        API[FastAPI]
        Ingest[PDF Ingestion]
        Chunk[Text Chunking]
        Embed[Embeddings]
        Chroma[ChromaDB]
        LLM[LLM Provider]
    end
    
    UI --> API
    Upload --> Ingest
    Chat --> API
    Ingest --> Chunk
    Chunk --> Embed
    Embed --> Chroma
    API --> LLM
    LLM --> Chroma
```

## Features

- PDF upload with automatic processing
- Intelligent document chunking
- Vector search with ChromaDB
- RAG endpoint with page citations
- Next.js frontend with chat interface
- Support for OpenAI-compatible LLM providers
- Accuracy evaluation with 10 test questions

## Getting Started

### With Docker Compose

```bash
cp .env.example .env
# Configure your API keys
docker-compose up --build
```

### Local Development

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
docsage/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── api/      # Endpoints
│   │   ├── services/ # PDF, Vector Store, LLM
│   │   └── config.py
│   └── tests/
├── frontend/         # Next.js frontend
│   └── src/
├── evals/            # System evaluation
└── docker-compose.yml
```

## API Endpoints

- `POST /api/upload` - Upload PDF
- `POST /api/ask` - Ask questions about documents
- `GET /health` - Health check

## Testing

```bash
cd backend
pytest tests/ -v
```

## License

MIT