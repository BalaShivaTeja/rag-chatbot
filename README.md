# RAG Chatbot

Minimal RAG (retrieval-augmented generation) chatbot using FastAPI, LangChain, ChromaDB, and OpenAI embeddings + Chat.

## Features

- Upload documents (.txt, .pdf) via `/ingest` -> build vector index
- Query via `/chat` -> returns answer + source snippets
- Simple React frontend
- Docker + docker-compose and GHCR CI action

## Quickstart

1. **Clone the repository**
```bash
git clone https://github.com/BalaShivaTeja/rag-chatbot.git
cd rag-chatbot
```

2. **Set up environment variables**
Copy `.env.example` to `.env` and add your OPENAI_API_KEY:
```bash
cp .env.example .env
# Edit .env and set OPENAI_API_KEY=sk-...
```

3. **Local dev (without Docker)**

Backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="sk-..."  # Or set in .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend:
```bash
cd frontend
npm install
npm run dev  # Opens at http://localhost:5173
```

4. **Local dev (with Docker Compose)**
```bash
cp .env.example .env  # Edit to set OPENAI_API_KEY
docker compose up --build
# Backend -> http://localhost:8000
# Frontend -> http://localhost:5173
```

## Usage

### Ingest Documents
Use the frontend upload form or curl:
```bash
curl -X POST "http://localhost:8000/ingest" -F "files=@./sample.pdf"
```

### Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What is in the document?"}'
```

## Project Structure

```
rag-chatbot/
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── ingest.py
│   │   └── retriever.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── docker-compose.yml
├── .github/workflows/ci-cd.yml
└── README.md
```

## Deployment

### GitHub Actions CI/CD
- The included workflow builds and pushes Docker images to GitHub Container Registry (GHCR)
- Set `GHCR_TOKEN` secret in your repository settings

### Deployment Options
- **Render / Railway / Fly.io**: Deploy the backend Docker image
- **VPS**: Run `docker-compose up` on your server
- **Managed platforms**: Connect repo and set `OPENAI_API_KEY` as environment variable

## Notes

- **Security**: Do NOT expose `OPENAI_API_KEY` publicly
- **Production**: Tighten CORS settings, secure the ingest endpoint, use persistent storage
- **Alternative Vector DBs**: Can swap Chroma for FAISS, Pinecone, Weaviate, etc.
- **Cost**: Monitor OpenAI API usage and costs

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `CHROMA_DIR`: Directory for vector database (default: `./chroma_db`)
- `MODEL_NAME`: OpenAI model to use (default: `gpt-4o-mini`)
- `VITE_API_BASE`: Frontend API base URL (default: `http://localhost:8000`)

## License

MIT
