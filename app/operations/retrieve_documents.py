from typing import Any, Dict, List

from app.integrations.vectormind_adapter import retrieve_documents_from_vectormind


def retrieve_documents(inputs: Dict[str, Any]) -> Dict[str, Any]:
    query = inputs.get("query")

    if not isinstance(query, str) or not query.strip():
        raise ValueError("retrieve_documents requires input {'query': <non-empty string>}")

    documents, raw_chunks = retrieve_documents_from_vectormind(query.strip(), k=10)

    retrieval_debug = {
        "query": query.strip(),
        "top_k": [
            {
                "rank": i,
                "score": chunk.get("score"),
                "source": chunk.get("metadata", {}).get("source"),
                "chunk_id": chunk.get("metadata", {}).get("chunk_id"),
                "text_preview": chunk["text"][:200] if chunk.get("text") else None,
            }
            for i, chunk in enumerate(raw_chunks)
        ],
    }

    return {"documents": documents, "retrieval_debug": retrieval_debug}
