# Healthcare AI Agent

Minimal demo project implementing a Retrieval-Augmented Generation (RAG) healthcare assistant.

This repository demonstrates:
- A small RAG agent that builds a FAISS index over documents and uses sentence-transformers for embeddings.
- A FastAPI HTTP wrapper exposing a /query endpoint for questions.
- A FHIR snippet showing how to fetch patient data from a FHIR server (demo only).
- Dockerfile and a basic CI workflow for running tests.

Warning: This is a demo project for learning and showcasing purposes only. Do NOT use this project in production or for clinical decision-making without appropriate clinical validation, security controls, and legal/compliance review.

Features
- RAG retrieval using sentence-transformers + FAISS
- OpenAI as default LLM backend (configurable via environment)
- Example Dockerfile to package the app
- CI: basic Python workflow to run tests / checks
- Example .env and instructions for secure secret management

Quick start (local)
1. Create a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Populate example docs or configure your data in `rag_agent.build_index(...)`.

4. Set your environment variables (example in `.env.example`):
   export OPENAI_API_KEY="sk-..."

5. Run the FastAPI app:
   uvicorn app:app --reload

6. Example request:
   curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d '{"question":"What is first-line medication for high blood pressure?"}'

Docker
- Build:
  docker build -t healthcare-ai-agent:latest .
- Run (ensure OPENAI_API_KEY is set):
  docker run -e OPENAI_API_KEY="$OPENAI_API_KEY" -p 8000:8000 healthcare-ai-agent:latest

CI
- A basic GitHub Actions workflow is included at `.github/workflows/ci.yml`. It installs dependencies and runs tests (you can add pytest tests in `tests/`).

License
- MIT License — see LICENSE file.

If you want, I will:
- Create the repository in your account once you grant repository-creation access, or
- Walk you through manual creation & push steps and then open a PR to add features (self-hosted LLM, FHIR sandbox integration, etc).