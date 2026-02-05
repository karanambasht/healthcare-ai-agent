"""
Simple FastAPI wrapper for the RAG agent. Keep all logs/audit externally.
Run:
uvicorn app:app --reload
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag_agent import RAGAgent

app = FastAPI(title="Healthcare RAG Agent - Demo")

# Example documents — replace with your trusted clinical sources
SAMPLE_DOCS = [
    {"id":"doc1","text":"Hypertension is defined as blood pressure greater than 140/90 mmHg. First-line treatment includes lifestyle modification and ACE inhibitors.", "meta":{}},
    {"id":"doc2","text":"ACE inhibitors can cause cough and angioedema; avoid in pregnancy.", "meta":{}},
    {"id":"doc3","text":"For diabetes mellitus type 2, metformin is first-line unless contraindicated.", "meta":{}},
]

agent = RAGAgent()
agent.build_index(SAMPLE_DOCS)

class Query(BaseModel):
    question: str
    user_id: str | None = None  # optional for audit

@app.post("/query")
def query_agent(req: Query):
    try:
        answer = agent.generate_answer(req.question)
        # TODO: store audit logs (user_id, question, retrieved doc ids, answer) securely
        return {"answer": answer, "note": "Demo only — not medical advice. Escalate to a clinician for clinical decisions."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
