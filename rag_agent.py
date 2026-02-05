"""
Minimal RAG agent:
- Builds a FAISS index from local documents
- Uses sentence-transformers for embeddings
- Calls OpenAI ChatCompletion for generation (default)
"""
from typing import List
import os
from sentence_transformers import SentenceTransformer
import faiss
import openai

MODEL_NAME = "all-MiniLM-L6-v2"
# embedding dimension for all-MiniLM-L6-v2 is 384
EMBED_DIM = 384

class RAGAgent:
    def __init__(self, model_name: str = MODEL_NAME):
        self.embedder = SentenceTransformer(model_name)
        self.index = None
        self.docs: List[dict] = []
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            openai.api_key = openai_api_key

    def build_index(self, docs: List[dict]):
        """
        docs: list of {"id": str, "text": str, "meta": {...}}
        """
        self.docs = docs
        texts = [d["text"] for d in docs]
        embeddings = self.embedder.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # Use inner-product index with normalized vectors for cosine similarity
        self.index = faiss.IndexFlatIP(EMBED_DIM)
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

    def retrieve(self, query: str, k: int = 5):
        q_emb = self.embedder.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        D, I = self.index.search(q_emb, k)
        results = []
        for idx in I[0]:
            if 0 <= idx < len(self.docs):
                results.append(self.docs[idx])
        return results

    def generate_answer(self, query: str, top_k: int = 4, max_tokens: int = 256) -> str:
        contexts = self.retrieve(query, top_k)
        if not contexts:
            return "No supporting documents found."

        context_text = "\n\n---\n\n".join([f"Source {c['id']}:\n{c['text']}" for c in contexts])
        prompt = f"""You are a clinical assistant. Use ONLY the provided source excerpts to answer the user's question.
If the answer is not supported in the sources, say "I don't know" and recommend escalation to a clinician.

SOURCES:
{context_text}

QUESTION:
{query}

Answer concisely, list supporting sources by id, and give recommended next steps.
"""
        if openai.api_key:
            resp = openai.ChatCompletion.create(
                model="gpt-4o" if hasattr(openai, "gpt-4o") else "gpt-4o-mini",
                messages=[{"role":"system","content":"You are a helpful clinical assistant."},
                          {"role":"user","content":prompt}],
                temperature=0.0,
                max_tokens=max_tokens,
            )
            if "choices" in resp and len(resp["choices"]) > 0:
                return resp["choices"][0]["message"]["content"].strip()
            return str(resp)
        else:
            return "OpenAI API key not configured. Set OPENAI_API_KEY."
