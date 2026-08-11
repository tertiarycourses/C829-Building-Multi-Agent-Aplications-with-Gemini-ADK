import hashlib
import math
import re

import chromadb

PASSAGES = [
    ("RB-BILL-01", "Duplicate card charges: collect both transaction references, timestamps, amount, and order ID. Do not promise a refund before reconciliation."),
    ("RB-AUTH-02", "Password reset: confirm the synthetic account ID, check whether the reset email was requested, and advise the user to inspect spam before escalation."),
    ("RB-API-03", "API timeout: record the correlation ID, endpoint, UTC time, and retry count. Retry only an idempotent request with bounded backoff."),
    ("RB-SEC-04", "Suspected account takeover: do not change contact details. Revoke active sessions and route to the account-security owner."),
]


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _embed(text: str, dimensions: int = 64) -> list[float]:
    vector = [0.0] * dimensions
    for token in _tokens(text):
        index = int(hashlib.sha256(token.encode()).hexdigest()[:8], 16) % dimensions
        vector[index] += 1.0
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


_client = chromadb.EphemeralClient()
_collection = _client.get_or_create_collection("supportops_runbooks", metadata={"hnsw:space": "cosine"})
if _collection.count() == 0:
    _collection.add(
        ids=[item[0] for item in PASSAGES],
        documents=[item[1] for item in PASSAGES],
        metadatas=[{"source": item[0]} for item in PASSAGES],
        embeddings=[_embed(item[1]) for item in PASSAGES],
    )


def search_knowledge(query: str, top_k: int = 2) -> dict:
    """Search the synthetic SupportOps runbook and return up to three source-labelled passages."""
    query = query.strip()
    if len(query) < 4:
        return {"status": "error", "error_type": "validation", "message": "Provide a more specific search query."}
    top_k = max(1, min(top_k, 3))
    result = _collection.query(query_embeddings=[_embed(query)], n_results=top_k)
    matches = [
        {"source": metadata["source"], "text": document, "distance": round(distance, 4)}
        for document, metadata, distance in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]
    return {"status": "success", "matches": matches}
